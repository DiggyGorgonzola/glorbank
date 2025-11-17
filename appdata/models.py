# models.py

from sqlalchemy import Column, Integer, String, DateTime, text, Boolean, LargeBinary, JSON
from .database import Base 
'''
User, Bank, Mail, Reports, OngoingTransaction, RegisteringOrganizations, Organization, Employees, Frozen
'''
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
