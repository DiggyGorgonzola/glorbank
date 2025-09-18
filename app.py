from flask import Flask, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, render_template, redirect, url_for, jsonify

users_db = {"Diggy Gorgonzola": "417"}
ip_db = {"Diggy Gorgonzola": 1}

app = Flask(__name__)
app.secret_key = "Glorbank"

  
@app.route('/', methods=["GET", "POST"])
def starting():
  return render_template("home.html")

@app.route('/indexi.html')
def indexi():
  return render_template("indexi.html")
  
@app.route('/register', methods=["GET", "POST"])
def register():
  return render_template("register.html", username_exists=False)

@app.route('/register_check', methods=["GET", "POST"])
def register_check():
  if request.method == "POST":
    username = request.form['username']
    password = request.form['password']
    if request.form['email']:
      email = request.form['email']
    if username in users_db:
      return render_template("register.html", username_exists="true")
    return render_template("home.html")
  return render_template("register,html", username_exists="false")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
      username = request.form['username']
      password = request.form['password']
      user_password_hash = users_db.get(username)
      if user_password_hash and users_db.get(username) == password:
        return render_template("indexi.html")
      return render_template("home.html", incorrect_password='false')
    else:
      return render_template("home.html", incorrect_password="true")

