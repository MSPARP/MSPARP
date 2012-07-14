from sqlalchemy import create_engine
from sqlalchemy.orm import backref, relation, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, UnicodeText, DateTime, Enum

import datetime

def now():
    return datetime.datetime.now()

engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
sm = sessionmaker(autocommit=False,
                  autoflush=False,
                  bind=engine)

Base = declarative_base()
Base.query = db_session.query_property()

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

Log.pages = relation(LogPage, backref='log')
