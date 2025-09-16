from flask import Flask, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, render_template, redirect, url_for

users_db = {"Diggy Gorgonzola": 417}

app = Flask(__name__)
app.secret_key = "Glorbank"
def check_password_hash(user_password_hash, password):
  if users_db[username] == password return True else False
@app.route('/', methods=["GET", "POST"])
def starting():
  return render_template("home.html")

@app.route('/indexi.html')
def indexi():
  return render_template("indexi.html")
  
@app.route('/home.html', methods=["GET", "POST"])
def index():
  if request.method == "POST":
    username = request.form['username']
    password = request.form['password']
    user_password_hash = user_db.get(username)
    if user_password_hash and check_password_hash(user_password_hash, password):
      return render_template("indexi.html")
  return render_template("home.html")

