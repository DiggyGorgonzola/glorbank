# models.py
import wrapped_print
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, text, Boolean, LargeBinary, JSON, Float
from .database import Base

'''
User, Bank, Mail, Reports, OngoingTransaction, RegisteringOrganizations, Organization, Signatures, Frozen
'''
db = SQLAlchemy()
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
  employer_org_id = db.Column(db.Integer, nullable=True)
  job_id = db.Column(db.Integer, nullable=True)

class Bank(Base):
  __tablename__ = "Bank"
  id = db.Column(db.Integer, primary_key=True)
  woolong = db.Column(db.String, nullable=False)
  parts = db.Column(db.String, nullable=False)
  credit = db.Column(db.String, nullable=False)
  accdate = db.Column(db.DateTime)
  national_id = db.Column(db.Integer, nullable=False, unique=True)
  tax_rate = db.Column(db.Integer, nullable=False)

class Mail(Base):
  __tablename__ = "Mail"
  id = db.Column(db.Integer, primary_key=True)
  acc_id_to = db.Column(db.Integer, nullable=False)
  title = db.Column(db.String, nullable=False)
  message = db.Column(db.String, nullable=False)
  contact = db.Column(db.String)

class OngoingTransactions(Base):
  __tablename__ = "OngoingTransactions"
  id = db.Column(db.Integer, primary_key=True)
  woolong = db.Column(db.String, nullable=False)
  information = db.Column(db.String, nullable=True)
  date = db.Column(db.DateTime)
  natid_from = db.Column(db.Integer, nullable=False, unique=True)
  natid_to = db.Column(db.Integer, nullable=False, unique=True)

class OngoingDepoWithdr(Base):
  __tablename__ = "OngoingDepoWithdr"
  id = db.Column(db.Integer, primary_key=True)
  withdraw_bool = db.Column(db.Boolean, nullable=False) # True = withdraw, False = deposit
  currency = db.Column(db.String, nullable=False)
  value = db.Column(db.Integer, nullable=False)
  natid = db.Column(db.Integer, nullable=False, unique=True)
  date = db.Column(db.DateTime, nullable=False)
  location = db.Column(db.String, nullable=False)
  information = db.Column(db.String, nullable=True)

# Organizations must go through a verification process before they are added to the actual database.
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
  email = db.Column(db.String(80), nullable=False)
  phone = db.Column(db.String, nullable=False)
  accdate = db.Column(db.DateTime, nullable=False)
  orgpass = db.Column(db.String, nullable=False)
  foundid = db.Column(db.Integer, nullable=False, unique=True)
  orgid = db.Column(db.String, unique=True, nullable=False)

class EmployeeType(Base):
  __tablename__ = "EmployeeType"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)
  orgid = db.Column(db.String, unique=False)

# For frozen users
class Frozen(Base):
  __tablename__ = "Frozen"
  id = db.Column(db.Integer, primary_key=True)
  national_id = db.Column(db.Integer, nullable=False, unique=True)

class Reports(Base):
  __tablename__ = "Reports"
  id = db.Column(db.Integer, primary_key=True)
  woolong = db.Column(db.String, nullable=False)
  information = db.Column(db.String, nullable=True)
  date = db.Column(db.DateTime)
  id_from = db.Column(db.String, nullable=False)
  id_to = db.Column(db.String, nullable=False)
  # fix whatever's wrong with this!



# non-bank-related models
class Signature(Base):
  __tablename__ = "Signature"
  id = db.Column(db.Integer, primary_key=True)
  signature = db.Column(db.String, nullable=False)
  national_id = db.Column(db.Integer, nullable=False, unique=False)

class LongAwait(Base):
  __tablename__ = "LongAwait"
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, nullable=False, unique=True)
  fails = db.Column(db.Integer, nullable=False)
  most_recent_fail = db.Column(db.DateTime, nullable=False)
