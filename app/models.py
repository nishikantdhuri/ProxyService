from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import Column,Integer,String,DateTime
from . import db

class User(UserMixin,db.Model):

    __tablename__='flasklogin-users'

    id = db.Column(Integer,primary_key=True)
    name= db.Column(String,nullable=False,unique=False)
    email=db.Column(String(40),nullable=False,unique=True)
    password=db.Column(String(200),nullable=False)
    last_login=db.Column(DateTime,nullable=True)

    def set_password(self,pwd):
        self.password = generate_password_hash(pwd,method='sha256')

    def check_password(self,password):
        return check_password_hash(self.password,password)

