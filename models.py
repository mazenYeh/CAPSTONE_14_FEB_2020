import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json


database_path = os.environ['DATABASE_URL']
# database_path = "postgres://gvfqcmnyvybbuk:4f753f507fa24736846c136fb5ca7c7b897f23462bffcdd9d0a0425034358222@ec2-52-202-185-87.compute-1.amazonaws.com:5432/d1vj4ufa22k8h8"

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Trainer(db.Model):  
    __tablename__ = 'Trainers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)

#   def __init__(self, name, catchphrase=""):
#     self.name = name
#     self.catchphrase = catchphrase

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def commit(self):
        db.session.commit()

class Client(db.Model):
    __tablename__ = 'Clients'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def commit(self):
        db.session.commit()

class Session(db.Model):
    __tablename__ = 'Sessions'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    trainer_id = Column(Integer)
    client_id = Column(Integer)
    date = Column(DateTime)

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def commit(self):
        db.session.commit()