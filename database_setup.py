import sys
import os 
from sqlalchemy import Column, ForeignKey, Integer, String 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

#create instance of declarative_base class 
Base = declarative_base()

# User Table for login information

class User(Base):
    # representing our table inside the database
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True) 
    name = Column(String(250), nullable = False)    
    email = Column(String(250), nullable = False)
    picture = Column(String(250))
     

#We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
       
       return {
           'name'         : self.name,
           'email'        : self.email,
           'picture'      : self.picture,
           'id'           : self.id,
       }
 
# Catalog Table
class Category(Base):
    #representing our table inside the database
    __tablename__ = 'category'
    id = Column(Integer,primary_key = True)
    name = Column(String(80),nullable = False)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

#We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
       
       return {
           'id'           : self.id,
           'name'         : self.name,
           
       }      
        

# Item Table
class CategoryItem(Base):
    # representing our table inside the database
    __tablename__ = 'categoryitem'
    title = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    category_id = Column(Integer,ForeignKey('category.id'))
    category = relationship(Category, backref='items') 
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

#We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
       
       return {
           'title'         : self.title,
           'description'   : self.description,
           'id'            : self.id,
           'category_id'   : self.category_id,
       }
 



######## insert at end of file ########
engine = create_engine('sqlite:///catalogitemwithusers.db')

Base.metadata.create_all(engine)



