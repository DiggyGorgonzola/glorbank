# Fetch.py

from flask import Blueprint, request, jsonify
from appdata.database import Base, engine, DATABASE_URL, start_session
from appdata.models import User, Bank, Mail, Reports, OngoingTransactions, RegisteringOrganizations, Organization, Frozen
from program.InfoGet import InfoGet
import appdata.signatures
LS = appdata.signatures.LoginSignatures
start_session()

fetch = Blueprint('fetch', __name__)

class Fetches:
  #dubious function
  #should be used instead of jsonify I think due to its shorthandedness...
  def json_out(status, received, **kwargs):
    v = {'status':status, 'received':received}
    for key,value in kwargs.items():
      v[key] = value
    return jsonify(v)

  
  @fetch.route('/usermail', methods=["GET","POST"])
  def handlemail():
    if request.method == 'POST':
      received_data = request.json
      try:
        return Fetches.json_out("success", received_data, response=InfoGet.getMail(received_data["useraccount"][0]))
      except Exception as error:
        return Fetches.json_out("failure", received_data, response=error.lower())
    return None
  
  @fetch.route("/dropsigmas", methods=["POST", "GET"])
  def dropSigmas():
    if request.method == "POST":
      received_data = request.json
      LS.deleteAllSignatures()
      try:
        return Fetches.json_out("success", received_data, response="Gilbert")
      except Exception as error:
        return Fetches.json_out("failure", received_data, response=error.lower())
    return None

