# money_handle.py

import wrapped_print
from flask import Blueprint, request, jsonify
from appdata.database import Base, engine, DATABASE_URL, start_session
from appdata.models import User, Bank, Mail, Reports, OngoingTransactions, RegisteringOrganizations, Organization, Frozen, Signature, EmployeeType
from program.InfoGet import InfoGet
from CBI import cbidict
import appdata.signatures, json
LS = appdata.signatures.LoginSignatures
session = start_session()

class MoneyHandle:

  def createDeposit(deposit_value=0, currency_type="Woolong", user_national_id=""):
    pass

  def verifyDeposit(teller_national_id, deposit_id)
    pass
