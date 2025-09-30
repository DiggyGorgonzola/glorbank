from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
import os, datetime


USERDATABASE = [
  ["Diggy Gorgonzola", "417", None, "127.0.0.1", datetime.datetime.now(), 1, -1],
  ["Dinky Gonky", "brd52009", None, "127.0.0.1", datetime.datetime.now(), 0, 1],
  ["Dinky Gonky Alt", "brd52009", None, "127.0.0.1", datetime.datetime.now(), 0, 2],
]

BANKDATABASE = [
  [-999999, USERDATABASE[0][4], USERDATABASE[0][6]],
  [5, USERDATABASE[1][4], USERDATABASE[1][6]],
  [-99999, USERDATABASE[2][4], USERDATABASE[2][6]],
]
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

class Bank(Base):
  __tablename__ = "Bank"
  id = db.Column(db.Integer, primary_key=True)
  bank_value = db.Column(db.Integer, nullable=False)
  accdate = db.Column(db.DateTime)
  national_id = db.Column(db.Integer, nullable=False, unique=True)

class OngoingTransactions(Base):
  __tablename__ = "OngoingTransactions"
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime)
  natid_from = db.Column(db.Integer, nullable=False, unique=True)
  natid_to = db.Column(db.Integer, nullable=False, unique=True)


# activate db
engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)


# create session
Session = sessionmaker(bind=engine)
session = Session()
session.begin()

#Add a basic database for testing purposes
existing_user = session.query(User).first()
existing_bankacc = session.query(Bank).first()

if not existing_user:
  for user in USERDATABASE:
      new_user = User(
          username=user[0],
          password=user[1],
          email=user[2],
          ip=user[3],
          accdate=user[4],
          admin=user[5],
          national_id=user[6]
      )
      session.add(new_user)
      session.commit()
if not existing_bankacc:
  for bankacc in BANKDATABASE:
    new_bankacc = Bank(
      bank_value=bankacc[0],
      accdate=bankacc[1],
      national_id=bankacc[2]
    )
    session.add(new_bankacc)
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
    nationalID = request.form['national']
    user = None
    bank = None
    for element in session.query(User).filter_by(username=username):
      user = element
    if user == None:
      return render_template("home.html", incorrect_password='true')
    #See if the credentials are valid. (WIP add IP 2fa)
    if user.password != password or user.national_id != nationalID:
      return render_template("home.html", incorrect_password='true')


    elif user.password == password and user.national_id == natioanlID:
      for element in session.query(Bank).filter_by(national_id=user.national_id):
        bank = element
      return render_template("indexi.html", useracc=[user.id, user.username, user.password, user.email, user.ip, user.accdate, user.admin, user.national_id], adming=user.admin, bankacc=[bank.id, bank.bank_value, bank.accdate, bank.national_id])
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

        # Make sure to hide the database based off of Admin capabilities~!
        database_list.append([element.id, element.username, element.password, element.email, element.ip, element.accdate, element.admin, element.national_id])
      return render_template("adminpanel.html", database=database_list)
    return render_template("register.html", typed_info=[], errror="Uh oh!")
  return render_template("register.html", typed_info=[], errror="Uh oh!")
#Base.metadata.drop_all(engine)
#DELETES THE ENTIRE DATABASE
