def addMessage(db,chatid,color,acronym,text):
	# generate encoded form
	message='%s#%s%s%s' % (color,acronym,(': ' if acronym else ''),text)
	# Save to the chat- list. This is the permanent log form
	messagesCount=db.rpush('chat-'+chatid,message)
	# Push to the publication channel to wake up longpolling listeners
	db.publish('channel-'+chatid,'%d#%s' % (messagesCount-1,message))

def addSystemMessage(db,chatid,text):
	addMessage(db,chatid,'000000','',text)
