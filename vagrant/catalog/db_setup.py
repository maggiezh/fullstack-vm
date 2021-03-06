import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    username = Column(String(250), nullable=False)
    email = Column(String(250), nullable = False)

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Item(Base):
    __tablename__ = 'category_item'
    id = Column(Integer, primary_key = True)
    itemName = Column(String(80), nullable = False)
    description = Column(String(500))

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'itemName': self.itemName,
            'description': self.description,
            'category_id': self.category_id
        }

#######insert at end of File ##############

#engine = create_engine('sqlite:///catalog.db')

# NOTE: to create the database:
# sudo -u postgres psql
# postgres=# create database postgres_catalog;
# postgres=# create user udacity with encrypted password 'n0pedy';
# postgres=# grant all privileges on database postgres_catalog to udacity;
engine = create_engine('postgresql://catalog:catalog@localhost/catalogMngr')

Base.metadata.create_all(engine)
