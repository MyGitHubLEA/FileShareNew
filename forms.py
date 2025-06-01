# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from _init_ import db
from models import Users
from  wtforms.validators import Length, Regexp
import re

class RegistrationForm(FlaskForm):
    login = StringField('Login', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired(), 
                                                     Length(min=8, max=100)])
    password2 = PasswordField(
        'Repeat your password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
 
    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError("")
        if not re.search(r'[0-9]', password.data):
            raise ValidationError("")
        if password.data is None:
            raise ValidationError("")
        

class LoginForm(FlaskForm):
    login = StringField('Login', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    def validate_password(self, extra):
        return self.password != '' and self.login != ''
