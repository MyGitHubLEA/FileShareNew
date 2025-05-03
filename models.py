from typing import Optional
from sqlalchemy import Column, Integer, String
import sqlalchemy as sa
import sqlalchemy.orm as so
from _init_ import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from _init_ import login

class Users(UserMixin, db.Model):
   id = Column(Integer, primary_key=True, autoincrement = True)
   login = Column(String, index=True, unique=True)
   password_hash = Column(String)
   
   def set_password(self, password):
       self.password_hash = generate_password_hash(password)

   def check_password(self, password):
       return check_password_hash(self.password_hash, password)

   def __repr__(self):
       return '<User {}>'.format(self.login)



@login.user_loader
def load_user(id):
  return db.session.get(Users, int(id))