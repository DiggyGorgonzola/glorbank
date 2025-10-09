# app.py

from flask import Flask, render_template, request, redirect, url_for, jsonify
from decimal import Decimal as decimal
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text, Boolean, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
import os, datetime


USERDATABASE = [
  ["Diggy Gorgonzola", "417", None, "127.0.0.1", datetime.datetime.now(), 10, -1],
  ["Dinky Gonky", "brd52009", None, "127.0.0.1", datetime.datetime.now(), 0, 1],
  ["Dinky Gonky Alt", "brd52009", None, "127.0.0.1", datetime.datetime.now(), 0, 2],
]

BANKDATABASE = [
  ["-999999", USERDATABASE[0][4], USERDATABASE[0][6]],
  ["5", USERDATABASE[1][4], USERDATABASE[1][6]],
  ["-99999", USERDATABASE[2][4], USERDATABASE[2][6]],
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
  bank_value = db.Column(db.String, nullable=False)
  accdate = db.Column(db.DateTime)
  national_id = db.Column(db.Integer, nullable=False, unique=True)

class OngoingTransactions(Base):
  __tablename__ = "OngoingTransactions"
  id = db.Column(db.Integer, primary_key=True)
  information = db.Column(db.String, nullable=True)
  date = db.Column(db.DateTime)
  natid_from = db.Column(db.Integer, nullable=False, unique=True)
  natid_to = db.Column(db.Integer, nullable=False, unique=True)

# Organizations must go through a verification process before they are added to the actual database.
class RegisteringOrganizations(Base):
  __tablename__ = "RegisteringOrganizations"
  id = db.Column(db.Integer, primary_key=True)
  accdate = db.Column(db.DateTime)
  name = db.Column(db.String, nullable=False)
  email = db.Column(db.String, nullable=False)
  phone = db.Column(db.String, nullable=False)


class Organization(Base):
  __tablename__ = "Organization"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(80), nullable=True)
  accdate = db.Column(db.DateTime)
  orgid = db.Column(db.String, unique=True, nullable=False)

# Perhaps make a separate table for each organization. Procedurally.
class Employees(Base):
  __tablename__ = "Employees"
  id = db.Column(db.Integer, primary_key=True)
  organization = db.Column(db.String, nullable=False)
  primary_owner = db.Column(db.String, nullable=True)
  secondary_owners = db.Column(db.String, nullable=True)
  org_admins = db.Column(db.String, nullable=True)
  org_employees = db.Column(db.String, nullable=True)

class Reports(Base):
  __tablename__ = "Reports"
  id = db.Column(db.Integer, primary_key=True)
  money = db.Column(db.String, nullable=False)
  information = db.Column(db.String, nullable=True)
  date = db.Column(db.DateTime)
  id_from = db.Column(db.String, nullable=False)
  id_to = db.Column(db.String, nullable=False)
  # fix whatever's wrong with this!


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


#Add a predefined database for testing purposes
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
  print([user.username, user.password, user.email, user.ip, user.accdate, user.admin, user.national_id])


def error(error_msg, user_info=[], redirect="home.html"):
  return render_template(redirect, error=error_msg, info=user_info)
#Collects info about personal accounts based on the admin's level
def admin_info_collect(admin_level):
  database_list = []
  for element in session.query(User).all():
    stringy = []
    if admin_level > 0:
      stringy.append(element.id)
      stringy.append(element.username)
    if admin_level > 1:
      stringy.append(element.password)
    else:
      stringy.append("HIDDEN")
    if admin_level > 0:
      stringy.append(element.email)
    if admin_level > 1:
      stringy.append(element.ip)
    else:
      stringy.append("HIDDEN")
    if admin_level > 0:
      stringy.append(element.accdate)
      stringy.append(element.admin)
    if admin_level > 1:
      stringy.append(element.national_id)
    else:
      stringy.append("HIDDEN")
    if admin_level > 2:
      print(element.national_id)
      gooner = session.query(Bank).filter_by(national_id=element.national_id).first()
      stringy.append(gooner.bank_value)
    else:
      stringy.append("HIDDEN")
    database_list.append(stringy)
  return database_list
  
#Collects reports based on the admin's level
def admin_reports_collect(admin_level):
  database_list = []
  for element in session.query(Reports).all():
    stringy = [element.id]
    if admin_level > 3:
      stringy.append(element.money)
    else:
      stringy.append("HIDDEN")
    if admin_level > 2:
      stringy.append(element.information)
    else:
      stringy.append("HIDDEN")
    if admin_level > 2:
      stringy.append(element.date)
    else:
      stringy.append("HIDDEN")
    if admin_level > 2:
      stringy.append(element.id_from)
    else:
      stringy.append("HIDDEN")
    if admin_level > 2:
      stringy.append(element.id_to)
    else:
      stringy.append("HIDDEN")
    database_list.append(stringy)
  return database_list
    # FINISH???

def admin_pending_orgs_collect(admin_level):
  database_list = []
  for element in session.query(RegisteringOrganizations).all():
    stringy = [element.id, element.accdate, element.name, element.email, element.phone]
    database_list.append(stringy)
  return database_list

#function 0 uhhh change this when we get a real home page
@app.route('/', methods=["GET", "POST"])
def home():
  return render_template("home.html", info=["", "", ""])


@app.route('/login', methods=["GET", "POST"])
# function 1
def login():
  global username, password, nationalID, user_ip, email
  if request.method == "POST":

    #Save data entered from the form
    username = request.form['username']
    password = request.form['password']
    nationalID = request.form['national']
    user = None
    bank = None
    user_info = [username, password, nationalID]
    try:
      nationalID = int(nationalID)
    except:
      return error("The username, password, or national ID provided is incorrect.", user_info=user_info)
    for element in session.query(User).filter_by(username=username):
      user = element
    if user == None:
      return error("The username, password, or national ID provided is incorrect.", user_info=user_info)
    
    #See if the credentials are valid. (WIP add IP 2fa)
    print(user.national_id, nationalID)
    print(type(user.national_id), type(nationalID))
    if user.password != password or user.national_id != nationalID:
      return error("The username, password, or national ID provided is incorrect.", user_info=user_info)


    elif user.password == password and user.national_id == nationalID:
      for element in session.query(Bank).filter_by(national_id=user.national_id):
        bank = element
      return render_template("indexi.html", useracc=[user.id, user.username, user.password, user.email, user.ip, user.accdate, user.admin, user.national_id], adming=user.admin, bankacc=[bank.id, bank.bank_value, bank.accdate, bank.national_id])
    return error("Something went wrong. ~ 1.2", user_info=user_info)  # <-- error code 1.2
  return render_template("home.html", info=["", "", ""])
  
@app.route('/register', methods=["GET", "POST"]) # In the middle of adding error checks for this function. Please make sure this works properly. All html files should store inputted data as "info", not "user_info" or "typed_data", otherwise the error function will not work!!!!!
#function 2
def register():
  global username, password, nationalID, user_ip, email
  if request.method == "POST":
    
    #Save data entered from the form
    username = request.form['username']
    password = request.form['password']
    nationalID = int(request.form['national'])
    user_ip = request.remote_addr
    email = ""
    if request.form['email']:
      email = request.form['email']

    #print data for testing purposes
    print((username, user_ip, password, email))
    user_info = [username, password, nationalID, email]

    #Add the user to the database. Check if the username is already taken
    try:
      new_user = User(username=username, password=password, ip=user_ip, email=email, accdate=datetime.datetime.now(), national_id=nationalID, admin=0)
    except:
      return error("Invalid data entered. ~ 2.1", user_info=user_info, redirect="register.html")  # <-- error code 2.1
    if session.query(User).filter_by(username=username).first():
      return error("Username or national ID entered is already registered. Please choose different values for these. ~ 2.1.1", user_info=user_info, redirect="register.html")
    elif session.query(User).filter_by(national_id=nationalID).first():
      return error("Username or national ID entered is already registered. Please choose different values for these. ~ 2.1.2", user_info=user_info, redirect="register.html")
    else:
      try:
        session.add(new_user)
      except:
        return error("Database error. ~ 2.2", user_info=user_info, redirect="register.html")
      else:
        session.commit()
        new_bank = Bank(bank_value=0, accdate=session.query(User).filter_by(national_id=nationalID).first().accdate, national_id=nationalID)
        session.add(new_bank)
        session.commit()
        return render_template("register.html", info=[username, password, nationalID, email], skinky="Your account has been registered!")
  return render_template("register.html", info=[])

@app.route('/register/organization', methods=["GET", "POST"])
# function 6
def regorg():
  if request.method == "POST":
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    try:
      new_org = RegisteringOrganizations(name=name, email=email, phone=phone, accdate=datetime.datetime.now())
    except:
      return error("Invalid data entered. ~ 6.1", user_info=[name, email, phone], redirect="organization_register.html")
    try:
      session.add(new_org)
      session.commit()
    except:
      return error("Something wrong happened. ~ 6.2", user_info=[name, email, phone], redirect="organization_register.html")
    return render_template("organization_register.html", info=[name, email, phone], skinky="Your organization has been added to the registration list! Please wait until an official from the Glorbenian National Bank contacts you.")
  elif request.method == "GET":
    return render_template("organization_register.html", info=[])
  return error("Something wrong happened. ~ 6.3", user_info=[], redirect="organization_register.html")



@app.route('/accountpage/adminpanel', methods=["GET", "POST"])
# function 3
def adminlink():
  if request.method == "POST":
    username = request.form['username']
    print(username)
    admin_capabilities = int(request.form['admin_capabilities'])
    print(admin_capabilities)
    if session.query(User).filter_by(username=username).first().admin == admin_capabilities:
      database_list = admin_info_collect(admin_capabilities)
      admin_user = session.query(User).filter_by(username=username).first()
      return render_template("adminpanel.html", admin_user=[admin_user.id, admin_user.username, admin_user.password, admin_user.email, admin_user.ip, admin_user.accdate, admin_user.admin, admin_user.national_id], database=database_list)
    return error("HACKER. ~ 3.1", user_info=[], redirect="register.html")
  return error("Something wrong happened. ~ 3.2", user_info=[], redirect="register.html")


@app.route('/accountpage/adminpanel/addmoney',methods=["GET", "POST"])
# function 4
def addmoney():
  database_list = []
  if request.method == "POST":
    admin_username = request.form["admins_username"]
    admin_user = session.query(User).filter_by(username=admin_username).first()

    bank_val = request.form['bankval']
    bank_val = decimal(bank_val)
    account_ID = request.form['account_ID']
    print(bank_val, account_ID)
    print(type(bank_val))
    user = session.query(User).filter_by(id=account_ID).first()
    user_bank = session.query(Bank).filter_by(national_id=user.national_id).first()
    if user_bank:
      user_bank.bank_value = str(decimal(user_bank.bank_value) + bank_val)
      new_report = Reports(money=str(bank_val), information=f"Done manually via Admin Panel by {admin_user.username}", date=datetime.datetime.now(), id_from=admin_user.national_id, id_to=user.national_id) 
      session.add(new_report)
      session.commit()
    print(user)
    database_list = admin_info_collect(admin_user.admin)
    return render_template("adminpanel.html", admin_user=[admin_user.id, admin_user.username, admin_user.password, admin_user.email, admin_user.ip, admin_user.accdate, admin_user.admin, admin_user.national_id], database=database_list)
  return render_template("adminpanel.html", admin_user=[admin_user.id, admin_user.username, admin_user.password, admin_user.email, admin_user.ip, admin_user.accdate, admin_user.admin, admin_user.national_id], database=database_list)


@app.route('/accountpage/reports', methods=["GET", "POST"])
# function 5
def reports():
  database_list = []
  if request.method == "POST":
    username = request.form['username']
    admin_user = session.query(User).filter_by(username=username).first()
    print(username)
    admin_capabilities = int(request.form['admin_capabilities'])
    print(admin_capabilities)
    if session.query(User).filter_by(username=username).first().admin == admin_capabilities:
      database_list = admin_reports_collect(admin_capabilities)
    return render_template("reports.html", admin_user=[admin_user.id, admin_user.username, admin_user.password, admin_user.email, admin_user.ip, admin_user.accdate, admin_user.admin, admin_user.national_id], database=database_list)
  return error("Something wrong happened. ~ 5.1", user_info=[], redirect="register.html")


@app.route('/login/organization', methods=["GET", "POST"])
# function 7
def logorg():
  # FINISH THIS !!!
  if request.method == "POST":
    pass
  elif request.method == "GET":
    return render_template("organization_login.html", info=[])
  return error("Something evil happened. ~ 7.1", user_info=[], redirect="home.html")

@app.route('/accountpage', methods=["GET", "POST"])
# function 8
def accountpage():
  if request.method == "POST":
    username = request.form['username1']
    password = request.form['password1']
    nationalID = request.form['national1']
    user = None
    bank = None
    user_info = [username, password, nationalID]
    try:
      nationalID = int(nationalID)
    except:
      return error("National ID must be an integer. ~ 8.1", user_info=user_info, redirect="home.html")
    for element in session.query(User).filter_by(username=username):
      user = element
    if user == None:
      return error("Account doesn't exist. ~ 8.2", user_info=user_info, redirect="home.html")
    #See if the credentials are valid. (WIP add IP 2fa)
    ''' FOUR HUNDRED AND SEVENTEEN!!!!
    %%###%%%%#(#%@@@@&&&&&&&&&&&&&%%%%%&&%%%#######%%%&&@@@@&%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%&&&@@&&&&@@&%%#((//******,,,,,,,*,*/#%&@%%%%&&@@&%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%@@@&@@&%%%%###((///******************//(#%&&&&&@&%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%&@@@&%%%#%%%###((/////****,,,,,,,,,,,***/((((%&&&@&%%%%%%%&&&&&%&&&&&&%
    %%%%%%%%%@@@&%###((///*****,,,,***********,,,,,****/((##%&&@&%%&&&&&&&%%%%%%%&&&
    %%%%%%%%&@@@&&&&&&&&&&%#(/**,,,,,**********,,*****///((((#&@@&%%%%&&&&&&&&&&&&&&
    %%%%%%%%&@&&&&%%###(((((((((/*,,,,,********//(##%%%&&&%%%%&@@&%&%%%&&&&&&&&&&&&&
    %%%%%%%%@@&&%%####((((##(((((/***********//(((///////((#%&&@@&&&&&&&&&&&&&&&&&&&
    %%%%%%%&@&%%########(#########(((///////((##((((//////(((#%&@&&&&&&&&&&&&&&&@@@@
    %%%%%%%&&%%%####(#%%#(**/%######(/////((###(((//****/(((((#%&&&&&&&&&&&&&@@@@@@@
    %%%%%%%%%%###%&&#*.,., ./###(((/**,,,,**//(##/,.,.,*(&&%(((#%&&&&&&&&&&&@@@@@@@@
    %%%%%%%%%#####%%/,(@&&&(,,((//***,,,,,,,,*//,.(&%%%*.(&#((((%&&&&&&&&&@@@@@@@@@@
    %%%%%%%%%##(//(#%#((#(((/*********,,,,**,,,***/#%#/**((/**/(%&&&&&&&&@@@@@@@@@@@
    &&&&&&&%%#(//***//((((/*****////**,,,,****,,,*/(####(*,,,*/(%&&&&&&&&@@@@@@@@@@@
    &&&&&&&%%#((/*************/////***,,,,,***,,,,,,,,,,,,,,,*/#&&&&&&&&&@@@@@@@@@@@
    &&&&&&&%%%#((/****,,,*****/////**,,,,,,****,,,,,,,,,,,,,*/(#%&&&&&&&@@@@@@@@@@@@
    &&&&&&&%%%%##(//*********///****,,,....,,,*,,,,,,,,,,,*//((#%&&&&&&&&&&@@@@@@@@@
    &&&&&&&&%%%%##((///*****/(#(((//***,,,,,*///*,,,,,,,**//(###%&&&&&&&&&&&&&@@@@@@
    &&&&&&&&&&%%%%##((//**/*(##%&&&%##(((/(%&@%#/,,*,,**//(###%%&&&&&&&&&&&&&&&&&@@@
    &&&&&&&&&&&&&&%%#(((///**/(/*/(#%%%##(((*,***,,,,**//(##%%%&&&&&&&&&&&&&&&&&&@@@
    %%%%%%%%%%&&&&&%%##((///*****,,***,,,,,,,,,,,,,***/(##%%%%%#(//(((((#####%&&&&@@
    /(#####((##%&&&&%%%##((////****,,,,,,,,,,,,,,**//(##%%%%(/(#/*/(/*/(//*/(/*/%&@@
    (((##((#(###%%&&&&&%%%#((((((/**,,,,,,********/(##%%%%#(((#(/((////////((/*,,,*#
    ##(###(###(##%&&&&&%%%%%%%##/**,,,,,,,,,**((((##%%%%#((((##(#(/((///////********
    (##(##((######&&&&&&&%&&&%#((//**,,,,,,***/(#%%%%%#####((#((#//((/*///(/*//*****
    (#%###########&&&&&&&&&&&&&&&&&&&%%%%&&&&&&%%%%%%%##(#%%#(/((//((////((**//,****
    (#%%#########%%&&&&&&&&&&&&&&&&&&&&&&&@@&&&&&%%%###((#%%#/*(((((/*//((///(/****/
    #(#%#((#######%%&&&&&&&&&&&&&&%%%%%&&&&&&&&&%%%%###(#%%#(////(((/**/((///((/*//(
    ###%##((#######%%&&%%&&&%#(#%&%%###%&&%####%%%%##(((#%%(////((((//(#(////((///(#
    ###%%##(((##%%#%%%%%&%&&%#////(#(###(//(((#%%%##(((#%#(//////(#(//(#(////(((///(
    ((##%%(((((##&&%%%%%%%%&%#//**,,,,,,,*///(#%%#####%%#((((//((#(//(((/////(((//((
    (######(((###%&%%#%%%%&&&%(///*******/((/(####(##%%%(/((////(((((/////(((##(//(#
    '''
    print(user.national_id, nationalID)
    print(type(user.national_id), type(nationalID))
    if user.password != password or user.national_id != nationalID:
      return error("Invalid credentials. ~ 8.3", user_info=user_info, redirect="home.html")


    elif user.password == password and user.national_id == nationalID:
      for element in session.query(Bank).filter_by(national_id=user.national_id):
        bank = element
      return render_template("indexi.html", useracc=[user.id, user.username, user.password, user.email, user.ip, user.accdate, user.admin, user.national_id], adming=user.admin, bankacc=[bank.id, bank.bank_value, bank.accdate, bank.national_id])

@app.route('/accountpage/pending_organizations', methods=["GET", "POST"])
def organizations():
  if request.method == "POST":
    admin_username = request.form["username"]
    admin_capababilities = request.form["admin_capabilities"]
    try:
      admin_capabilities = int(admin_capababilities)
    except:
      pass
    admin_user = session.query(User).filter_by(username=admin_username).first()
    if admin_user.admin == admin_capabilities:
      database_list = []
      database_list = admin_pending_orgs_collect(admin_user.admin)
      return render_template("pending_orgs.html", admin_user=[admin_user.id, admin_user.username, admin_user.password, admin_user.email, admin_user.ip, admin_user.accdate, admin_user.admin, admin_user.national_id], database=database_list)

#Base.metadata.drop_all(engine)
#DELETES THE ENTIRE DATABASE
