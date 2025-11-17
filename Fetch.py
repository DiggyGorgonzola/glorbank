# fetch.py
from app import InfoGet
#if there is an error it is probably gonna be in line 2. Importing app might make it freak out.
from flask import Flask, render_template, request, redirect, url_for, jsonify, Blueprint
fetch = Blueprint('fetch', __name__, template_folder='templates', static_folder='static')
print("This might not work lmao")

class Fetches:
  def __init__():
    return None

  #dubious function
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
        mail_unread = InfoGet.getMail(received_data['useraccount'][0]
        return json_out("success", received_data, response=mail_unread)
      except Exception as error:
        return json_out("failure", received_data, response=error.lower())
    return None

  @fetch.route('/getuser', methods=["GET", "POST"]
  def getuser():
    if request.method == 'POST':
      recieved_data = request.json
      try:
        user_account = [i for i in InfoGet.List(session,query(User).filter_by(id=received_data["id"])
        return json_out("success", received_data, response=user_account)
      except Exception as error:
        return json_out("failure", received_data, response=error.lower())
    return None
