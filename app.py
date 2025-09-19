from flask import Flask, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, render_template, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

users_db = {"Diggy Gorgonzola": "417"}
ip_db = {"Diggy Gorgonzola": (1)}
users_emails = {"Diggy Gorgonzola": "bendole3141592@gmail.com"}

app = Flask(__name__)
app.secret_key = "Glorbank"

'''
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
print(app.config['SQLALCHEMY_DATABASE_URI'])
'''

# I'm not sure what to do with the stuff above.
  
@app.route('/', methods=["GET", "POST"])
def starting():
    if request.method == "POST":
      username = request.form['username']
      password = request.form['password']
      user_password_hash = users_db.get(username)
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
      if username not in users_db.keys():
        print((username, user_ip, password, email))
        users_db[username] = password
        ip_db[username] = user_ip
        users_emails[username] = email
        return render_template("home.html")
      return render_template("register.html", username_exists="true")
    else:
      return render_template("register.html")



