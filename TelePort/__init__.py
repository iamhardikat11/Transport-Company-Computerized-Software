from flask import Flask,session
# from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_session import Session
from flask_migrate import Migrate
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TelePort.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///TelePort.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://wixpnsmxofsmoo:b83766cfaa394bbd0dc88889caf7b6b7b38f947c4ef8d7142c5cb11c724c0906@ec2-107-22-122-106.compute-1.amazonaws.com:5432/d8jkgtpjhv5fnm'
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
bcrypt = Bcrypt(app)
log_manage = LoginManager(app)
from TelePort import routes
