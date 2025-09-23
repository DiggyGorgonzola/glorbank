from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
import os

# create the db link
app = Flask(__name__)
Base = declarative_base()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# create the db and encryption
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# base db
users_db = {"Diggy Gorgonzola": "417"}
ip_db = {"Diggy Gorgonzola": (1)}
users_emails = {"Diggy Gorgonzola": "bendole3141592@gmail.com"}

app.secret_key = "Glorbank"


# db traits
class User(Base):
  __tablename__ = 'User'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(80), unique=True)
  ip = db.Column(db.Text)


# activate db
engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)


# create session
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/', methods=["GET", "POST"])
def starting():
  if request.method == "POST":
    username = request.form['username']
    password = request.form['password']
    try:
      user = session.query(User).filter_by(username=username)
      print(user)
    except:
      return render_template("home.html", incorrect_password='true')
    if user_password_hash and users_db.get(username) == password:
      return render_template("indexi.html")
    return render_template("home.html", incorrect_password='true')
  else:
    return render_template("home.html")

@app.route('/indexi.html')
def indexi():
  return render_template("indexi.html")
  
@app.route('/register', methods=["GET", "POST"])
def register():
  if request.method == "POST":
    username = request.form['username']
    password = request.form['password']
    user_ip = request.remote_addr
    email = None
    if request.form['email']:
      email = request.form['email']

    print((username, user_ip, password, email))
    new_user = User(username=username, password=password, ip=user_ip, email=email)
    with engine.begin() as conn: # WIP (see if username exists in User)
      he = conn.execute(text('SELECT username FROM User'))
    for row in he:
      print(row)
    if not session.query(User).filter_by(username=username):
      session.add(new_user)
      session.commit()
      return render_template("home.html")
    return render_template("register.html", username_exists="true")
  else:
    return render_template("register.html")



