#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/5/26 15:15
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 03.py
 Description:
 Software   : PyCharm
"""
from sqlalchemy.orm import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String
class User(Base):
    __tablename__ = 'user_account'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    # nickname = Column(String)

    def __repr__(self):
       return "<User(name='%s', fullname='%s')>" % (
                            self.name, self.fullname)

print(User.__table__)

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


config_info={
    'user':'root',
    'password':'root',
    'host':'localhost',
    'port':3306,
    'dbname':'seo'
}
content_sql="mysql+mysqldb://{user}:{password}@{host}/{dbname}".format(**config_info)
engine=create_engine(content_sql)
Session=sessionmaker(bind=engine)
session=Session()
user_data={
    'id':50,
    'name':'hike',
    'fullname':'haidong'
}
ed_user=User(**user_data)
# session.add(ed_user)

select_user=session.query(User).filter_by(name="hike").first()
session.commit()
print(select_user)