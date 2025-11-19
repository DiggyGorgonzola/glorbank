# Fetch.py

from flask import Blueprint, request, jsonify
from appdata.database import Base, engine, DATABASE_URL, start_session
from appdata.models import User, Bank, Mail, Reports, OngoingTransactions, RegisteringOrganizations, Organization, Frozen, Signature
from program.InfoGet import InfoGet
import appdata.signatures
LS = appdata.signatures.LoginSignatures
session = start_session()

fetch = Blueprint('fetch', __name__)

#if there is an error it is probably gonna be in line 2. Importing app might make it freak out.
class Fetches:
  #dubious function
  #should be used instead of jsonify I think due to its shorthandedness...
  def json_out(status, received, **kwargs):
    v = {'status':status, 'received':received}
    for key,value in kwargs.items():
      v[key] = value
    return jsonify(v)

  
  @fetch.route('/usermail', methods=["GET","POST"])
  def handleMail():
    if request.method == 'POST':
      received_data = request.json
      try:
        return Fetches.json_out("success", received_data, response=InfoGet.getMail(received_data["useraccount"][0]))
      except Exception as error:
        return Fetches.json_out("failure", received_data, response=error.lower())
    return None
  
  @fetch.route("/dropsigmas", methods=["GET","POST"]) #mainly for testing purposes
  def dropSigmas():
    if request.method == 'POST':
      received_data = request.json
      LS.deleteAllSignatures()
      try:
        return Fetches.json_out("success", received_data, response="Gilbert") # <- idk man
      except Exception as error:
        return Fetches.json_out("failure", received_data, response=error.lower())
    return None

  @fetch.route("/getacc", methods=["GET","POST"])
  def getAcc():
    if request.method == 'POST':
      received_data = request.json
      print(received_data)
      signature_instance = session.query(Signature).filter_by(signature=received_data).first()
      print(InfoGet.List(signature_instance))
      if signature_instance:
        user = InfoGet.List(session.query(User).filter_by(national_id=signature_instance.national_id).first())
        print(f"NATIONAL ID: {signature_instance.national_id}")
        print(InfoGet.List(user))
        try:
          return Fetches.json_out("success", received_data, response=user) # <- idk man
        except Exception as error:
          return Fetches.json_out("failure", received_data, response=error.lower())
      else:
        return Fetches.json_out("failure", received_data, response="signature doesn't exist!") #<- create a catch block or smth
    return None
