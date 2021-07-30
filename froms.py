from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import data_required,ValidationError,EqualTo
from flask import render_template,flash,request,redirect,url_for
from test.models import User
from test import bcrypt,db
from flask_login import login_user


class RegistrationForm(FlaskForm):
    username=StringField('username',validators=[data_required()])
    password = PasswordField('password', validators=[data_required()])
    confirm_password=PasswordField('confirm_password',validators=[data_required(),EqualTo('password',message="password must be same")])
    submit=SubmitField('submit')
    def validate_on_submit(self,username,password):
        #hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
    def validate_username(self,username):
        user=User.query.filter_by(username=username).first()
        if user:
            return render_template('registereduser.html')

class LoginForm(FlaskForm):
    username=StringField('username',validators=[data_required()])
    password=PasswordField('password',validators=[data_required()])
    remember=BooleanField('Remember me')
    submit=SubmitField('Submit')
         #   print("wrong username and password")




