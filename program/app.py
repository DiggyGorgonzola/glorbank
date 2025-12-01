# app.py
import wrapped_print

from flask import Flask, render_template, request, redirect, url_for, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

from decimal import Decimal as decimal

from appdata.database import Base, engine, DATABASE_URL, start_session
from appdata.models import User, Bank, Mail, Reports, OngoingTransactions, RegisteringOrganizations, Organization, Signature, Frozen, EmployeeType
from appdata.models import Signature
import appdata.signatures
from CBI import cbidict, HOMEREDIRECT
from program.InfoGet import InfoGet
from program.Fetch import fetch
import os, datetime, json

LS = appdata.signatures.LoginSignatures

NONEARRAY = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
USERDATABASE = [
  ["Diggy Gorgonzola", "417", "bendole3141592@gmail.com", "127.0.0.1", datetime.datetime.now(), 1000, -1, 1, 1],
  ["Dinky Gonky", "brd52009", None, "127.0.0.1", datetime.datetime.now(), 2, 1, 1, 1],
  ["Dinky Gonky Alt", "brd52009", None, "127.0.0.1", datetime.datetime.now(), 0, 2, 1, 1],
]
USERMAIL = [
  [1, 1, "TITLE", "MESSAGE", "CONTACT"],
  [2, 1, "TITLE", "MESSAGE", "CONTACT"],
  [3, 1, "TITLE", "MESSAGE", "CONTACT"],
]
BANKDATABASE = [
  [USERDATABASE[0][4], USERDATABASE[0][6], "999999", "99999", "999999"],
  [USERDATABASE[1][4], USERDATABASE[1][6], "0", "0", "0"],
  [USERDATABASE[2][4], USERDATABASE[2][6], "0", "0", "0"],
]
ORGANIZATIONDATABASE = [
  ["G.N.B.", "bendole3141592@gmail.com", "3253497795", datetime.datetime.now(), "Glorbenia", -1, 1]
]
ETDATABASE = [
  ["Teller", 1],
  ["Teller2", 1],
  ["Teller3", 1],
]
STM = False
STATIC_FOLDER = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), "static")
TEMPLATES_FOLDER = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), "templates")



app = Flask(__name__, static_folder=STATIC_FOLDER, template_folder=TEMPLATES_FOLDER)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL  # SQLite file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = STM
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.secret_key = "Glorbank" # change this for safety
Base.metadata.create_all(bind=engine)


app.register_blueprint(fetch)


session = start_session()

#print the database for testing purposes
for user in session.query(User).all():
  print(str(InfoGet.List(user)))
for signature in session.query(Signature).all():
  print(str(InfoGet.List(signature)))
for org in session.query(Organization).all():
  print(str(InfoGet.List(org)))
print(InfoGet.List(session.query(Organization).filter_by(orgid=1).first()))
'''BuildDb is mainly for testing purposes. It creates a pre-existing SQL database if it doesn't already exist'''
def BuildDb():
  #Add a basic database for testing purposes
  existing_user = session.query(User).first()
  existing_bankacc = session.query(Bank).first()
  existing_usermail = session.query(Mail).first()
  existing_signature = session.query(Signature).all()
  existing_organization = session.query(Organization).first()
  existing_employee_type = session.query(EmployeeType).first()
  if not existing_employee_type:
    for et in ETDATABASE:
      new_et = EmployeeType(
        name=et[0],
        orgid=et[1]
      )
      session.add(new_et)
      session.commit()
  if not existing_organization:
    for org in ORGANIZATIONDATABASE:
      new_org = Organization(
        name=org[0],
        email=org[1],
        phone=org[2],
        accdate=org[3],
        orgpass=org[4],
        foundid=org[5],
        orgid=org[6]
      )
      session.add(new_org)
      session.commit()
  if not existing_user:
    for user in USERDATABASE:
        new_user = User(
            username=user[0],
            password=user[1],
            email=user[2],
            ip=user[3],
            accdate=user[4],
            admin=user[5],
            national_id=user[6],
            employer_org_id=user[7],
            job_id=user[8]
        )
        session.add(new_user)
        session.commit()
  if not existing_bankacc:
    for bankacc in BANKDATABASE:
      new_bankacc = Bank(
        accdate=bankacc[0],
        national_id=bankacc[1],
        woolong=bankacc[2],
        parts=bankacc[3],
        credit=bankacc[4]
      )
      session.add(new_bankacc)
      session.commit()   
  if not existing_usermail:
    for mail in USERMAIL:
      new_mail = Mail(
        acc_id_to=mail[1],
        title=mail[2],
        message=mail[3],
        contact=mail[4]
      )
      session.add(new_mail)
      session.commit()
  if existing_signature:
    for sig in existing_signature:
      session.delete(sig)
      session.commit()
BuildDb()

# Figure this stuff out? <- Maybe should go to Fetches!
@app.route('/goto', methods=["GET", "POST"])
def goto():
  if request.method == "POST":
    redirect = request.form['redirect']
    info=[request.form['username'],request.form['password'],request.form['national']]
    print(info)
    return render_template(redirect, info=info)
  return error("HELP", user_info=['', '', ''])

def Delete():
  Base.metadata.drop_all(engine)
  print("Deleting Database...")
#DELETES THE ENTIRE DATABASE

def transact(nidfrom, nidto, amt):
  print("HAAAAIII")
  bank_accountfrom = session.query(Bank).filter_by(national_id=nidfrom).first()
  bank_accountto = session.query(Bank).filter_by(national_id=nidto).first()


  print(InfoGet.List(bank_accountfrom))
  woolong_accountfrom = decimal(bank_accountfrom.woolong)
  woolong_accountto = decimal(bank_accountto.woolong)

  woolong_accountfrom -= decimal(amt)
  bank_accountfrom.woolong = int(woolong_accountfrom)

  woolong_accountto += decimal(amt)
  bank_accountto.woolong = int(woolong_accountto)
  session.commit()


def Index(national_id=None, signature=None):
  model_signature = None
  if national_id is not None:
    model_signature = session.query(Signature).filter_by(national_id=national_id).first()
  elif signature is not None:
    model_signature = session.query(Signature).filter_by(signature=signature).first()
  model_signature = InfoGet.List(model_signature)[1]
  return render_template('indexi.html', signature=model_signature)

'''





+-----------------------+
| HTML ROUTES           |
+-----------------------+
'''
@app.route('/error', methods=["GET", "POST"])
def error(error_msg="", /, user_info=NONEARRAY, redirect=HOMEREDIRECT):
  print(redirect)
  return render_template("error.html", error=error_msg, info=user_info, redirect=redirect)

class Routes:
  # USE fetch() FOR EVERYTHING HERE!!!!
  # THE FETCH REVOLUTION, NOVEMBER 17TH 2025!!!!
  # ITS SOOOO COOOOOOL


  #Dumb function we have a lot of work to do huh?


  #function 0 uhhh change this when we get a real home page
  @app.route('/', methods=["GET", "POST"])
  def home():
    return render_template("home.html", info=["", "", ""])

  @app.route('/login', methods=["GET", "POST"])
  # function 1
  def login():
    if request.method == "POST":

      #Save data entered from the form (We can used Fetches for this!
      username = request.form['username']
      password = request.form['password']
      nationalID = request.form['national']
      user, bank = None, None
      user_info = [username, password, nationalID]
      try:
        nationalID = int(nationalID)
      except:
        return render_template("home.html", error="The username, password, or national ID provided is incorrect. ~ 1.1.0", info=user_info)
      for element in session.query(User).filter_by(username=username):
        user = element
      if user == None:
        return render_template("home.html", error="The username, password, or national ID provided is incorrect. ~ 1.1.1", info=user_info)
      
      #See if the credentials are valid. (WIP add IP 2fa)
      print(user.national_id, nationalID)
      print(type(user.national_id), type(nationalID))
      if user.password != password or user.national_id != nationalID:
        return render_template("home.html", error="The username, password, or national ID provided is incorrect. ~ 1.1.2", info=user_info)


      elif user.password == password and user.national_id == nationalID:
        for element in session.query(Bank).filter_by(national_id=user.national_id):
          bank = element
        LS.createSignature(nationalID)
        signature = session.query(Signature).filter_by(national_id=nationalID).first()
        for i in session.query(Signature).all():
          print("HELLO HELLO HELLO HELLO", [i.signature, i.national_id])
          #, mail_unread=InfoGet.getMail(user.id)
        return Index(national_id=nationalID)
      return error("Something went wrong. ~ 1.2", redirect="home.html", user_info=user_info)  # <-- error code 1.2
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
      user_ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()
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
          new_bank = Bank(woolong=0, parts=0, credit=0, accdate=session.query(User).filter_by(national_id=nationalID).first().accdate, national_id=nationalID)
          session.add(new_bank)
          session.commit()
          return render_template("register.html", info=[username, password, nationalID, email], skinky="Your account has been registered!")
    return render_template("register.html", info=[])

  @app.route('/register/organization', methods=["GET", "POST"])
  # function 6
  def regorg():
    if request.method == "POST":
      name = request.form["name"]
      password = request.form["password"]
      email = request.form["email"]
      phone = request.form["phone"]
      foundernat = request.form["foundernat"]
      founderpass = request.form["founderpass"]
      try:
        new_org = RegisteringOrganizations(name=name, email=email, phone=phone, accdate=datetime.datetime.now(), orgpass=password)
      except:
        return error("Invalid data entered. ~ 6.1", user_info=[name, password, email, phone, foundernat, founderpass], redirect="organization_register.html")
      #try:
      session.add(new_org)
      session.commit()
      #except:
        #return error("Something wrong happened. ~ 6.2", user_info=[name, password, email, phone, foundernat, founderpass], redirect="organization_register.html")
      return render_template("organization_register.html", info=[name, password, email, phone, foundernat, founderpass], skinky="Your organization has been added to the registration list! Please wait until an official from the Glorbenian National Bank contacts you.")
    elif request.method == "GET":
      return render_template("organization_register.html", info=[])
    return error("Something wrong happened. ~ 6.3", redirect="organization_register.html")

  @app.route('/accountpage/adminpanel', methods=["GET", "POST"])
  # function 3
  def adminlink():
    if request.method == "POST":
      username = request.form['username']
      admin_capabilities = int(request.form['admin_capabilities'])
      if 'addwoolong' in request.form.keys():
        try:
          acc = session.query(Bank).filter_by(id=request.form['account']).first()
          acc.woolong = str(decimal(acc.woolong) + decimal(request.form['addwoolong']))
          session.commit()
        except:
          return error("You entered an invalid number", redirect="adminpanel.html")
      if session.query(User).filter_by(username=username).first().admin == admin_capabilities:
        database_list = InfoGet.accCollect(admin_capabilities, session.query(User).all())
        admin_user = session.query(User).filter_by(username=username).first()
        return render_template("adminpanel.html", admin_user=InfoGet.List(admin_user), database=database_list)
      return error("HACKER. ~ 3.1", redirect="register.html")
    return error("Something wrong happened. ~ 3.2", redirect="register.html")


  @app.route('/accountpage/datasheets', methods=["GET", "POST"])
  def datasheets():
    if request.method == "POST":
      datasheet = request.form['datasheet']
      stuff = request.form["admin_user"].split(",")
      username = stuff[1]
      admin_capabilities = stuff[4]
      user = session.query(User).filter_by(username=username).first()
      database_list,database_keys = [],[]
      if user.admin == int(admin_capabilities):
        database_list = [InfoGet.ListCensor(i) for i in session.query(globals()[datasheet]).all()]
        database_keys = InfoGet.SQLattrs(session.query(globals()[datasheet]).first())
      print(database_keys)

      return render_template("datasheets.html", database=database_list, keys=database_keys, admin_user=InfoGet.List(user), type=datasheet)
    return render_template("home.html")

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
        user_bank.woolong = str(decimal(user_bank.woolong) + bank_val)
        new_report = Reports(woolong=str(bank_val), information=f"Done manually via Admin Panel by {admin_user.username}", date=datetime.datetime.now(), id_from=admin_user.national_id, id_to=user.national_id) 
        session.add(new_report)
        session.commit()
      print(user)
      database_list = InfoGet.accCollect(admin_user.admin, session.query(User).all())
      return render_template("adminpanel.html", admin_user=[i for i in InfoGet.List(admin_user)], database=database_list)
    return render_template("adminpanel.html", admin_user=[i for i in InfoGet.List(admin_user)], database=database_list)

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
        database_list = InfoGet.reportCollect(admin_capabilities, session.query(Reports).all())
      return render_template("reports.html", admin_user=[i for i in InfoGet.List(admin_user)], database=database_list)
    return error("Page not found. ~ -1", redirect="register.html")

  @app.route('/accountpage', methods=["GET", "POST"])
  # function 8
  def accountpage():
    if request.method == "POST":
      username = request.form['username']
      password = request.form['password']
      nationalID = request.form['national']
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
      #See if the credentials are valid. (WIP add IP 2fa)
      print(user.national_id, nationalID)
      print(type(user.national_id), type(nationalID))
      if user.password != password or user.national_id != nationalID:
        return error("Invalid credentials. ~ 8.3", user_info=user_info, redirect="home.html")


      elif user.password == password and user.national_id == nationalID:
        for element in session.query(Bank).filter_by(national_id=user.national_id):
          bank = element
        return Index(national_id=nationalID)
    return error("Page not found", redirect="register.html")

  @app.route('/accountpage/sendmoney', methods=["GET", "POST"])
  # gooner function lmao
  def sendmoney():
    if request.method == "POST":
      value = request.form["num_woolong"]
      sendto = request.form["account_to_transfer"]
      sendfrom = request.form["nationalid"]
      user = request.form['user']
      sendfrom = int(sendfrom)
      user = int(user)
      if sendfrom == user:
        accountfrom = session.query(User).filter_by(national_id=sendfrom).first()
        accountto = session.query(User).filter_by(id=sendto).first()
        if int(value) < cbidict["suspicious_transaction_limit"]:
          transact(accountfrom.national_id, accountto.national_id, value)

          transaction_report = Reports(woolong=str(value), information=f"{accountfrom.username} gave {accountto.username} {str(value)} woolong.", date=datetime.datetime.now(), id_from=accountfrom.national_id, id_to=accountto.national_id)
          session.add(transaction_report)
          session.commit()
          new_mail = Mail(acc_id_to=accountfrom.id, title="Transaction Information", message=f"    At {datetime.datetime.now().strftime("%I:%M %p, %A, %B %d, %Y")} you have sent {value} Woolong to another bank account.\n\n    If you believe this to be an error, please send a message to the gmail provided below.", contact="bendole3141592@gmail.com (main provider of the G.N.B. service).")
          session.add(new_mail)
          session.commit()
        else:
          pending_transaction = OngoingTransactions(woolong=value, information=f"{accountfrom.username} wishes to make a transaction with {accountto.username}", date=datetime.datetime.now(), natid_from=accountfrom.national_id, natid_to=accountto.national_id)
          session.add(pending_transaction)
          session.commit()
      else:
        print("Something bad happened")
      print(value)
      print(sendfrom)
      signature = [InfoGet.List(i) for i in session.query(Signature).all()]
      print(signature)
      signature2 = session.query(Signature).filter_by(national_id=sendfrom).first()
      print("USER:", InfoGet.List(signature))
      return render_template("indexi.html", signature=InfoGet.List(signature2)[1])
    return error("Page not found", redirect="register.html")
  @app.route('/login/organization', methods=["GET", "POST"])
  # function 7
  def logorg():
    # FINISH THIS !!!
    if request.method == "POST":
      pass
    elif request.method == "GET":
      return render_template("organization_login.html", info=[])
    return error("Page not found. ~ -1", redirect="register.html")
  # function 9
  @app.route('/accountpage/pending_organizations', methods=["GET", "POST"])
  def organizations():
    if request.method == "POST":
      admin_username = request.form["username"]
      admin_capabilities = request.form["admin_capabilities"]
      try:
        admin_capabilities = int(admin_capabilities)
      except:
        pass
      admin_user = session.query(User).filter_by(username=admin_username).first()
      if admin_user.admin == admin_capabilities:
        database_list = []
        database_list = InfoGet.pendOrgCollect(admin_user.admin, session.query(RegisteringOrganizations).all())
        return render_template("pending_orgs.html", admin_user=[i for i in InfoGet.List(admin_user)], database=database_list)
    return error("Page not found", redirect="register.html")

  # function 10
  @app.route('/accountpage/withdraw', methods=["GET", "POST"])
  def withdraw():
    if request.method == "POST":
      return error("We haven't done this yet! ~ 10.1")
    return error("Page not found", redirect="register.html")
