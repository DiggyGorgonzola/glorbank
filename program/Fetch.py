# Fetch.py

import wrapped_print
from flask import Blueprint, request, jsonify
from appdata.database import Base, engine, DATABASE_URL, start_session
from appdata.models import User, Bank, Mail, Reports, OngoingTransactions, RegisteringOrganizations, Organization, Frozen, Signature
from program.InfoGet import InfoGet
from CBI import cbidict
import appdata.signatures, json
LS = appdata.signatures.LoginSignatures
session = start_session()

fetch = Blueprint('fetch', __name__)

class Fetches:


  @fetch.route("/GNB", methods=["GET", "POST"])
  def GNB():
    if request.method == 'POST':
      received_data = request.json
      if received_data in list(cbidict.keys()):
        return jsonify({"success":"success", "received_data":received_data, "response":cbidict[received_data]})
      return jsonify({"success":"failureT", "received_data":received_data, "response":"null"})
    return jsonify({"success":"failure: request method is GET", "received_data":received_data, "response":"null"})

  


  @fetch.route("/getacc", methods=["GET","POST"])
  def getAcc():
    if request.method == 'POST':
      print(request.json)
      received_data = request.json["signature"]
      get_model = request.json["model"]
      print(get_model)
      signature_instance = session.query(Signature).filter_by(signature=received_data).first()
      if signature_instance and get_model == "User":
        user = InfoGet.List(session.query(User).filter_by(national_id=signature_instance.national_id).first())
        return jsonify({"success":"success", "received_data":received_data, "response":user})
      elif signature_instance and get_model == "Bank":
        bank = InfoGet.List(session.query(Bank).filter_by(national_id=signature_instance.national_id).first())
        return jsonify({"success":"success", "received_data":received_data, "response":bank})
      else:
        return jsonify({"success":"failure", "received_data":received_data, "response":"null"})
    return jsonify({"success":"failure: request method is GET", "received_data":received_data, "response":"null"})
