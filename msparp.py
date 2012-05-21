from flask import Flask,g,request,render_template,make_response,redirect,url_for,jsonify,abort
from redis import Redis
from uuid import uuid4
from collections import defaultdict
import itertools,re,time
from characters import CHARACTER_GROUPS,CHARACTERS
from quirks import QUIRKS
from reaper import getTime
from messages import addMessage,addSystemMessage
from werkzeug.routing import BaseConverter,ValidationError
class ChatIDConverter(BaseConverter):
	def __init__(self,url_map):
		super(ChatIDConverter,self).__init__(url_map)
	def to_python(self,value):
		if re.match('^[-a-zA-Z0-9]+$',value):
			return value
		else:
			raise ValidationError()
	def to_url(self,value):
		return value
app = Flask(__name__)
app.url_map.converters['chat']=ChatIDConverter

class User(object):
	ATTRIBUTES=['acronym','name','color','character','picky']
	VALIDATORS={
			'acronym':re.compile('^[a-zA-Z0-9?*]*$'),
			'name':re.compile('^[^\0-\x1F]+$'),
			'color':re.compile('^[0-9a-fA-F]{6}$'),
			'character':re.compile('^[a-z /]+$'),
		}
	def __init__(self,uid):
		self.uid=uid
		self.acronym='??'
		self.name='Anonymous'
		self.color='000000'
		self.character='anonymous/other'
		self.quirks=set()
		self.quirkargs=defaultdict(list)
		self.picky=False
		self.picky_characters=set()
		self.fresh=True

	def load(self,db):
		self.fresh=False
		prefix=self.prefix
		for attrib in User.ATTRIBUTES:
			v=db.get(prefix+attrib)
			if v is not None:
				if attrib in ('picky',):
					v=(v=='True')
				setattr(self,attrib,v)
		if self.picky:
			self.picky_characters=db.smembers(prefix+'picky-chars')
		else:
			self.picky_characters=db.smembers('all-chars')
		quirks=self.quirks=db.smembers(prefix+'quirks')
		qa=self.quirkargs=defaultdict(list)
		for q in quirks:
			qa[q]=db.lrange(prefix+'quirks-'+q,0,-1)
	
	def save(self,db):
		prefix=self.prefix
		for attrib in User.ATTRIBUTES:
			db.set(prefix+attrib,str(getattr(self,attrib)))
		db.sadd('all-users',self.uid)
		ckey=prefix+'picky-chars'
		if self.picky:
			db.delete(ckey)
			for char in self.picky_characters:
				db.sadd(ckey,char)
		else:
			db.sunionstore(ckey,('all-chars',))
		quirkey=prefix+'quirks'
		db.delete(quirkey)
		for quirk in self.quirks:
			db.sadd(quirkey,quirk)
		for key,values in self.quirkargs.items():
			rkey=quirkey+'-'+key
			if values:
				db.delete(rkey)
				for v in values:
					db.rpush(rkey,v)

	@property
	def prefix(self):
		return 'user-%s-'% self.uid
	
	def apply(self,form):
		for key,regex in User.VALIDATORS.items():
			if key in form:
				if regex.search(form[key]):
					setattr(self,key,form[key])
				else:
					raise ValueError(key)
		picky=self.picky='picky' in form
		if picky:
			chars=self.picky_characters=set(k[6:] for k in form.keys() if k.startswith('picky-'))
			if not chars:
				raise ValueError("No selected characters!")
		quirks=self.quirks=set(k[6:] for k in form.keys() if k.startswith('quirk-'))
		qa=self.quirkargs=defaultdict(list)
		for q in quirks:
			qa[q]=[value for (key,value) in sorted(form.items()) if key.startswith('qarg-'+q)]
	
	def buildQuirksFunction(self):
		wrap='text'
		qa=self.quirkargs
		vcount=itertools.count()
		args={}
		for q in self.quirks:
			values=qa.get(q,[])
			if values:
				params=[('qarg'+str(num),value) for (num,value) in itertools.izip(vcount,values)]
				args.update(dict(params))
				wrap='%s(%s,%s)' % (q,wrap,','.join(k for (k,v) in params))
			else:
				wrap='%s(%s)' % (q,wrap)
		return wrap,args

@app.before_request
def connect():
	# connect to database 
	db=g.db=Redis(host='localhost')

	# if the user has logged in, go ahead and load their user object
	uid=request.cookies.get('uid',None)
	if uid is not None:
		g.user=user=User(uid)
		user.load(db)
	else:
		g.user=None


def requireUser(func):
	"Redirect the user to the front page if they haven't logged in yet"
	def inner(*args,**kwargs):
		if g.user is None:
			return redirect(url_for('configure'))
		return func(*args,**kwargs)
	return inner


def parseLine(line,id):
	"Parse a chat line like 'FF00FF#Some Text' into a dict"
	parts=line.split('#',1)
	return {
		'id':id,
		'color':parts[0],
		'line':parts[1]
	}


		
	

def parseMessages(seq,offset):
	return jsonify(messages=[parseLine(line,i) for (i,line) in enumerate(seq,offset)])

def announceIfNew(chatid,uid):
	chatkey='chat-%s-users' % chatid
	if not g.db.sismember(chatkey,g.user.uid):
		g.db.sadd(chatkey,g.user.uid)
		addSystemMessage(g.db,chatid,'%s [%s] joined chat' % (g.user.name,g.user.acronym))

@requireUser
@app.route('/chat/<chat:chatid>')
def chat(chatid):
	announceIfNew(chatid,g.user.uid)

	existing_lines=[parseLine(line,0) for line in g.db.lrange('chat-'+chatid,0,-1)]
	latestNum=len(existing_lines)-1
	quirks_func,quirks_args=g.user.buildQuirksFunction()
	return render_template('chat.html',user=g.user,chatid=chatid,lines=existing_lines,latestNum=latestNum,applyQuirks=quirks_func,quirks_args=quirks_args)

def markAlive(chatid,uid):
	g.db.zadd('chats-alive',chatid+'/'+uid,getTime())	
	g.db.sadd('users-chatting',uid)

@requireUser
@app.route('/chat/<chat:chatid>/post',methods=['POST'])
def postMessage(chatid):
	addMessage(g.db,chatid,g.user.color,g.user.acronym,request.form['line'])
	markAlive(chatid,g.user.uid)
	return 'ok'

@requireUser
@app.route('/chat/<chat:chatid>/ping',methods=['POST'])
def pingServer(chatid):
	markAlive(chatid,g.user.uid)
	return 'ok'

@requireUser
@app.route('/chat/<chat:chatid>/messages')
def getMessages(chatid):
	after=int(request.args['after'])
	announceIfNew(chatid,g.user.uid)
	markAlive(chatid,g.user.uid)
	messages=g.db.lrange('chat-'+chatid,after+1,-1)
	if messages:
		return parseMessages(messages,after+1)
	g.db.subscribe('channel-'+chatid)
	for msg in g.db.listen():
		if msg['type']=='message':
			id,rest=msg['data'].split('#',1)
			return parseMessages([rest],int(id)) # TEST THIS

@requireUser
@app.route('/bye/searching')
def quitSearching():
	g.db.zrem('searchers',g.user.uid)
	return 'ok'

@requireUser
@app.route('/bye/chat/<chat:chatid>')
def quitChatting(chatid):
	g.db.sadd('quits',chatid+'/'+g.user.uid)
	return 'ok'

@requireUser
@app.route('/matches',methods=['POST'])
def findMatches():
	g.user.apply(request.form)
	g.user.save(g.db)
	uid=g.user.uid
	g.db.zadd('searchers',uid,getTime())
	g.db.publish('search-alert',uid)
	g.db.delete('chat-'+uid)
	return render_template("searching.html")

@requireUser
@app.route('/matches/foundYet')
def foundYet():
	target=g.db.get('chat-'+g.user.uid)
	if target:
		return jsonify(target=target)
	else:
		g.db.zadd('searchers',g.user.uid,getTime())
		abort(404)

@app.route("/")
def configure():
	if not g.user:
		g.user=user=User(str(uuid4()))
		user.save(g.db)
		
	res=make_response(render_template('frontpage.html',
		user=g.user,
		groups=CHARACTER_GROUPS,
		characters=CHARACTERS,
		default_char=g.user.character,
		quirks=QUIRKS,
		users_searching=g.db.zcard('searchers'),
		users_chatting=g.db.scard('users-chatting')
		)
	)
	res.set_cookie('uid',g.user.uid,max_age=365*24*60*60)
	return res

if __name__ == "__main__":
    app.run(port=8000,debug=True)
