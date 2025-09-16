from flask import Flask, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, render_template, redirect, url_for

users_db = {}

app = Flask(__name__)
app.secret_key = "Glorbank"
@app.route('/')
def starting():
  return render_remplate("home.html")
@app.route('/home.html')
def index():
  return render_template("home.html")
