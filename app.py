from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
import os, datetime

# create the db link
app = Flask(__name__)
Base = declarative_base()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# create the db and encryption
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#secret key!!!!
app.secret_key = "Glorbank"


# db traits
class User(Base):
  __tablename__ = "User"
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(80), unique=True)
  admin = db.Column(db.Boolean)
  ip = db.Column(db.Text)
  accdate = db.Column(db.DateTime)


# activate db
engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)


# create session
Session = sessionmaker(bind=engine)
session = Session()
session.begin()

#Add a base admin account for testing purposes
#try:
  #new_user = User(username="Diggy Gorgonzola", password="417", email=None, ip="127.0.0.1", accdate=datetime.datetime.now(), admin=True)
  #session.add(new_user)
  #session.commit()
#except:
  #session.rollback()

#print the database for testing purposes
#a = session.query(User).filter_by(username="Dinky Gonky")
#for user in a:
  #print([user.admin])


@app.route('/', methods=["GET", "POST"])
def starting():
  if request.method == "POST":

    #Save data entered from the form
    username = request.form['username']
    password = request.form['password']
    a = session.query(User).filter_by(username=username)
    for element in a:
      user = element

    #See if the credentials are valid. (WIP add IP 2fa)
    if user.password != password:
      return render_template("home.html", incorrect_password='true')
    elif user.password == password:

      #See if the user is an admin and go to admin panel
      if user.admin:
        liste = [[user.id, user.username, user.password, user.email, user.ip, user.accdate, user.admin] for user in session.query(User).all()]
        print(liste)
        return render_template("adminpanel.html", database=liste)
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
    
    #Save data entered from the form
    username = request.form['username']
    password = request.form['password']
    user_ip = request.remote_addr
    email = None
    if request.form['email']:
      email = request.form['email']

    #print data for testing purposes
    print((username, user_ip, password, email))

    #Add the user to the database. Check if the username is already taken
    new_user = User(username=username, password=password, ip=user_ip, email=email, accdate=datetime.datetime.now(), admin=False)
    if not session.query(User).filter_by(username=username).all():
      try:
        session.add(new_user)
      except:
        return render_template("register.html", error="true")
      else:
        session.commit()
        return render_template("home.html")
    return render_template("register.html", username_exists="true")
  return render_template("register.html")


#Base.metadata.drop_all(engine)
#DELETES THE ENTIRE DATABASE
