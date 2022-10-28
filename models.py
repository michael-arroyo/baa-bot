from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger

Base = declarative_base()

class News(Base):
    __tablename__ = 'news'
    newsMstId = Column(BigInteger, primary_key=True)
