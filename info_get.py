from flask import Flask, render_template, request, redirect, url_for, jsonify
from decimal import Decimal as decimal
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text, Boolean, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
import os, datetime
Base = declarative_base()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.secret_key = "Glorbank"
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
  woolong = db.Column(db.String, nullable=False)
  parts = db.Column(db.String, nullable=False)
  credit = db.Column(db.String, nullable=False)
  accdate = db.Column(db.DateTime)
  national_id = db.Column(db.Integer, nullable=False, unique=True)
class OngoingTransactions(Base):
  __tablename__ = "OngoingTransactions"
  id = db.Column(db.Integer, primary_key=True)
  information = db.Column(db.String, nullable=True)
  date = db.Column(db.DateTime)
  natid_from = db.Column(db.Integer, nullable=False, unique=True)
  natid_to = db.Column(db.Integer, nullable=False, unique=True)
class RegisteringOrganizations(Base):
  __tablename__ = "RegisteringOrganizations"
  id = db.Column(db.Integer, primary_key=True)
  accdate = db.Column(db.DateTime)
  name = db.Column(db.String, nullable=False)
  email = db.Column(db.String, nullable=False)
  phone = db.Column(db.String, nullable=False)
  orgpass = db.Column(db.String, nullable=False)
class Organization(Base):
  __tablename__ = "Organization"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(80), nullable=True)
  accdate = db.Column(db.DateTime)
  orgid = db.Column(db.String, unique=True, nullable=False)
class Employees(Base):
  __tablename__ = "Employees"
  id = db.Column(db.Integer, primary_key=True)
  organization = db.Column(db.String, nullable=False)
  primary_owner = db.Column(db.String, nullable=True)
  secondary_owners = db.Column(db.String, nullable=True)
  org_admins = db.Column(db.String, nullable=True)
  org_employees = db.Column(db.String, nullable=True)
class Frozen(Base):
  __tablename__ = "Frozen"
  id = db.Column(db.Integer, primary_key=True)
  national_id = db.Column(db.Integer, nullable=False, unique=True)
class Reports(Base):
  __tablename__ = "Reports"
  id = db.Column(db.Integer, primary_key=True)
  money = db.Column(db.String, nullable=False)
  information = db.Column(db.String, nullable=True)
  date = db.Column(db.DateTime)
  id_from = db.Column(db.String, nullable=False)
  id_to = db.Column(db.String, nullable=False)
engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
session.begin()


# I don't know if adding this stuff will work?
class InfoGet():
  def accCollect(admin_level, accs):
    database_list = []
    for element in accs:
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
      else:
        stringy.append("HIDDEN")
        stringy.append("HIDDEN")
        stringy.append("HIDDEN")
      database_list.append(stringy)
    return database_list
    
  #Collects reports based on the admin's level
  def reportCollect(admin_level, reports):
    database_list = []
    for element in reports:
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
  
  def pendOrgCollect(admin_level, orgs):
    database_list = []
    for element in orgs:
      stringy = [element.id, element.accdate, element.name, element.email, element.phone]
      database_list.append(stringy)
    return database_list
  
  def bankCollect(admin_level, accs):
    stringy = []
    for element in accs:
      print(element.national_id)
      stringy.append(element.woolong)
      stringy.append(element.parts)
      stringy.append(element.credit)
      database_list.append(stringy)
    return database_list
      
    
