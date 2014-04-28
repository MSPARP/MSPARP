from sqlalchemy import create_engine
from sqlalchemy.orm import backref, relation, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, UnicodeText, DateTime, Enum

import datetime
import os

def now():
    return datetime.datetime.now()

engine = create_engine(os.environ['MYSQL_URL'], convert_unicode=True, pool_recycle=3600, max_overflow=0, pool_size=50)
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
    log_id = Column(Integer, ForeignKey('logs.id'), primary_key=True, autoincrement=False)
    number = Column(Integer, primary_key=True)
    content = Column(UnicodeText, nullable=False)

Log.pages = relation(LogPage, backref='log')
