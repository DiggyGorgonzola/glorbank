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
  email = db.Column(db.String(80), nullable=True)
  admin = db.Column(db.Integer)
  ip = db.Column(db.Text)
  accdate = db.Column(db.DateTime)
  national_id = db.Column(db.Integer, nullable=False, unique=True)


# activate db
engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)


# create session
Session = sessionmaker(bind=engine)
session = Session()
session.begin()

#Add a base admin account for testing purposes
existing_user = session.query(User).first()

if not existing_user:
    new_user = User(
        username="Diggy Gorgonzola",
        password="417",
        email=None,
        ip="127.0.0.1",
        accdate=datetime.datetime.now(),
        admin=1,
        national_id = -1
    )
    session.add(new_user)
    session.commit()

#print the database for testing purposes
a = session.query(User).all()
for user in a:
  print([user.username, user.password, user.email, user.ip, user.accdate, user.admin])


@app.route('/', methods=["GET", "POST"])
def starting():
  global username, password, nationalID, user_ip, email
  if request.method == "POST":

    #Save data entered from the form
    username = request.form['username']
    password = request.form['password']
    user = None
    for element in session.query(User).filter_by(username=username):
      user = element
    if user == None:
      return render_template("home.html", incorrect_password='true')
    #See if the credentials are valid. (WIP add IP 2fa)
    if user.password != password:
      return render_template("home.html", incorrect_password='true')


    elif user.password == password:
      return render_template("indexi.html", useracc=[user.id, user.username, user.password, user.email, user.ip, user.accdate, user.admin, user.national_id], adming=user.admin)
    return render_template("home.html", incorrect_password='true')
  else:
    return render_template("home.html")
  
@app.route('/register', methods=["GET", "POST"])
def register():
  global username, password, nationalID, user_ip, email
  if request.method == "POST":
    
    #Save data entered from the form
    username = request.form['username']
    password = request.form['password']
    nationalID = request.form['national']
    user_ip = request.remote_addr
    email = ""
    if request.form['email']:
      email = request.form['email']

    #print data for testing purposes
    print((username, user_ip, password, email))

    #Add the user to the database. Check if the username is already taken
    try:
      new_user = User(username=username, password=password, ip=user_ip, email=email, accdate=datetime.datetime.now(), national_id=nationalID, admin=0)
    except:
      return render_template("register.html", typed_info=[], error="Uh Oh")
    if session.query(User).filter_by(username=username).first():
      return render_template("register.html", typed_info=[username, password, nationalID, email], username_exists="true")
    elif session.query(User).filter_by(national_id=nationalID).first():
      return render_template("register.html", typed_info=[username, password, nationalID, email], nationalID_exists="true")
    else:
      try:
        session.add(new_user)
      except:
        return render_template("register.html", typed_info=[], error="true")
      else:
        session.commit()
        return render_template("home.html")
  return render_template("register.html", typed_info=[])

# WIP WIP WIP WIP WIP WIP
@app.route('/adminlink', methods=["GET", "POST"])
def adminlink():
  if request.method == "POST":
    username = request.form['username']
    print(username)
    admin_capabilities = int(request.form['admin_capabilities'])
    print(admin_capabilities)
    if session.query(User).filter_by(username=username).first().admin == admin_capabilities:
      database_list = []
      for element in session.query(User).all():
        database_list.append([element.id, element.username, element.password, element.email, element.ip, element.accdate, element.admin, element.national_id])
      return render_template("adminpanel.html", database=database_list)
    return render_template("register.html", typed_info=[], errror="Uh oh!")
  return render_template("register.html", typed_info=[], errror="Uh oh!")
#Base.metadata.drop_all(engine)
#DELETES THE ENTIRE DATABASE
