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
session.begin()
session.rollback()
try:
  new_user = User(username="Diggy Gorgonzola", password="417", email=None, ip="127.0.0.1")
  session.add(new_user)
  session.commit()
except:
  session.rollback()
a = session.query(User).all()
for user in a:
  print([user.id, user.username, user.password, user.email, user.ip])
@app.route('/', methods=["GET", "POST"])
def starting():
  if request.method == "POST":
    username = request.form['username']
    password = request.form['password']
    if not session.query(User).filter_by(username=username).all():
      return render_template("home.html", incorrect_password='true')
    elif session.query(User).filter_by(username=username).all()[0].password == password:
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
    if not session.query(User).filter_by(username=username).all():
      try:
        session.add(new_user)
      except:
        session.rollback()
        return render_template("register.html", error="true")
      else:
        session.commit()
        return render_template("home.html")
    return render_template("register.html", username_exists="true")
  return render_template("register.html")



