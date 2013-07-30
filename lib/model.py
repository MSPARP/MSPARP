from sqlalchemy import create_engine
from sqlalchemy.orm import backref, relation, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, UnicodeText, DateTime, Enum

import datetime

def now():
    return datetime.datetime.now()

engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True, pool_recycle=3600)
sm = sessionmaker(autocommit=False,
                  autoflush=False,
                  bind=engine)

base_session = scoped_session(sm)

Base = declarative_base()
Base.query = base_session.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    url = Column(String(100), unique=True)
    page_count = Column(Integer, default=1)
    time_created = Column(DateTime(), nullable=False, default=now)
    time_saved = Column(DateTime(), nullable=False, default=now)

class LogPage(Base):
    __tablename__ = 'log_pages'
    log_id = Column(Integer, ForeignKey('logs.id'), primary_key=True)
    number = Column(Integer, primary_key=True)
    content = Column(UnicodeText, nullable=False)

class Chat(Base):
    __tablename__ = 'chats'
    log_id = Column(Integer, ForeignKey('logs.id'), primary_key=True)
    type = Column(Enum(u"saved", u"group", u"deleted", name=u"chats_type"), nullable=False, default=u"saved")
    counter = Column(Integer, nullable=False, default=1)
    topic = Column(UnicodeText, nullable=True)

class ChatSession(Base):
    __tablename__ = 'chat_sessions'
    log_id = Column(Integer, ForeignKey('logs.id'), primary_key=True)
    session_id = Column(String(36), primary_key=True)
    counter = Column(Integer, nullable=False)
    expiry_time = Column(DateTime(), nullable=False, default=now)
    group = Column(Enum(u"silent", u"user", u"mod3", u"mod2", u"mod", u"globalmod", name=u"chat_sessions_group"), nullable=False, default=u"user")
    # XXX UTF-8 ISSUES WITH LENGTH?!
    # XXX also check these lengths
    character = Column(Unicode(100), nullable=False, default=u"anonymous/other")
    name = Column(Unicode(100), nullable=False, default=u"Anonymous")
    acronym = Column(Unicode(15), nullable=False, default=u"")
    color = Column(Unicode(15), nullable=False, default=u"000000")
    case = Column(Enum(
        u"alt-lines",
        u"alternating",
        u"inverted",
        u"lower",
        u"normal",
        u"title",
        u"upper",
        name=u"chat_sessions_case"
    ), nullable=False, default=u"normal")
    replacements = Column(UnicodeText, nullable=False, default=u"[]")
    regexes = Column(UnicodeText, nullable=False, default=u"[]")
    quirk_prefix = Column(Unicode(50), nullable=False, default=u"")
    quirk_suffix = Column(Unicode(50), nullable=False, default=u"")

Log.pages = relation(LogPage, backref='log')
Log.chat = relation(Chat, backref='log', uselist=False)
Log.sessions = relation(ChatSession, backref='log')

