from flask import Flask, jsonify, request, send_file, render_template, send_from_directory, redirect, url_for, flash 
import requests 
import socket 
from minio import Minio
from dotenv import load_dotenv 
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from urllib.parse import urlsplit
import sqlalchemy as sa
from _init_ import db
from models import Users
from _init_ import app
from forms import RegistrationForm, LoginForm


@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    print("Sucsess")
    user = db.session.scalar(
      sa.select(Users).where(Users.login == form.login.data))
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data)
    return redirect(url_for('index')) 
  return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    #db.drop_all()  # Drop all tables (be careful!)
    #db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(login=form.login.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Ok')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



