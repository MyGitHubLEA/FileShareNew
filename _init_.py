from flask import Flask, jsonify, request, send_file, render_template, send_from_directory, redirect, url_for, flash 

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from dotenv import load_dotenv 
from flask_login import UserMixin

import os 

load_dotenv() 

LOCAL_FILE_PATH = os.environ.get('LOCAL_FILE_PATH') 
ACCESS_KEY = os.environ.get('ACCESS_KEY') 
SECRET_KEY = os.environ.get('SECRET_KEY')



app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '123')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database.db'

app.config.from_object(Config)
db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'

if not os.path.exists("files"):  os.makedirs("files")   
UPLOAD_FOLDER = 'uploads' 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
lock_get_file = False 
lock_load_file = True 
lock_status = False 
password = r"YOURPASSHERE"