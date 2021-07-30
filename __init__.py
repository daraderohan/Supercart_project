from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from selenium import webdriver
from flask_login import current_user
from sel import job
from selenium.webdriver.chrome.options import Options

app=Flask(__name__)
app.config['SECRET_KEY']='992a1aced4a729c428a4c94ee7f0fbd1'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
scheduler=APScheduler()
scheduler.init_app(app)
options=webdriver.ChromeOptions()
options.headless=True

from test import routes
#scheduler.add_job(func=job, trigger='interval', args=[current_user.username, current_user.password], id='job', seconds=15)






