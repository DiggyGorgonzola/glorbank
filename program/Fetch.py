# Fetch.py

import wrapped_print
from flask import Blueprint, request, jsonify
from appdata.database import Base, engine, DATABASE_URL, start_session
from appdata.models import User, Bank, Mail, Reports, OngoingTransactions, RegisteringOrganizations, Organization, Frozen, Signature, EmployeeType, OngoingDepoWithdr
from program.InfoGet import InfoGet
from CBI import cbidict
import appdata.signatures, json, datetime
LS = appdata.signatures.LoginSignatures
session = start_session()

fetch = Blueprint('fetch', __name__)

class Fetches:


  @fetch.route("/GNB", methods=["GET", "POST"])
  def GNB():
    received_data = None
    if request.method == 'POST':
      received_data = request.json
      if received_data in list(cbidict.keys()):
        return jsonify({"success":"success", "received_data":received_data, "response":cbidict[received_data]})
      return jsonify({"success":"failureT", "received_data":received_data, "response":"null"})
    return jsonify({"success":"failure: request method is GET", "received_data":received_data, "response":"null"})

  @fetch.route("/getacc", methods=["GET","POST"])
  def getAcc():
    received_data = None
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

  @fetch.route("/getorg", methods=["GET","POST"])
  def getOrg():
    received_data = None
    if request.method == "POST":
      print(request.json)
      received_data = int(request.json)
      print(InfoGet.List(session.query(Organization).filter_by(orgid=received_data).first()))
      return jsonify({"success":"success", "received_data":received_data, "response":InfoGet.List(session.query(Organization).filter_by(orgid=received_data).first())})
    return jsonify({"success":"failure: request method is GET", "received_data":received_data, "response":"null"})
  
  @fetch.route("/CDOW", methods=["GET", "POST"])
  def CDOW():
    received_data = None
    if request.method == "POST":
      received_data = request.json
      if received_data["select1"] == "deposit":
        print("DEPOSITING")
        k = OngoingDepoWithdr(
          withdraw_bool=False,
          currency=received_data["select3"],
          value=received_data["valuee"],
          natid=received_data["natid"],
          date=datetime.datetime.now(),
          location=received_data["select2"]
        )
        session.add(k)
        session.commit()
      elif received_data["select1"] == "withdraw":
        print("WITHDRAWING")
        k = OngoingDepoWithdr(
          withdraw_bool=True,
          currency=received_data["select3"],
          value=received_data["valuee"],
          natid=received_data["natid"],
          date=datetime.datetime.now(),
          location=received_data["select2"]
        )
        session.add(k)
        session.commit()
      return jsonify({"success":"success", "received_data":received_data, "response":received_data})
    return jsonify({"success":"failure: request method is GET", "received_data":received_data, "response":received_data})
  
  @fetch.route("/EmployeeTypes", methods=["GET", "POST"])
  def employeeTypes():
    received_data = None
    if request.method == 'POST':
      print(request.json)
      received_data = request.json
      print(received_data)
      employee_types = session.query(EmployeeType).filter_by(orgid=received_data).all()
      print(employee_types) 
      response = {"data":{i.id:InfoGet.List(i) for i in employee_types}, "keys":{i.id:InfoGet.SQLattrs(i) for i in employee_types}}
      print(response)
      return jsonify({"success":"success", "received_data":received_data, "response":response})
    return jsonify({"success":"failure: request method is GET", "received_data":received_data, "response":"null"})
