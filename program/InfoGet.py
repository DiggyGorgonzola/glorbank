
# InfoGet.py

import wrapped_print
from flask import Blueprint
from appdata.database import Base, engine, DATABASE_URL, start_session
from appdata.models import User, Bank, Mail, Reports, OngoingTransactions, RegisteringOrganizations, Organization, Frozen
from CBI import ALJ
session = start_session()

class InfoGet:

  '''SQLattrs lists all the attributes of the SQL class given'''
  def SQLattrs(obj):
    return [attr for attr in type(obj).__dict__ if not attr.startswith('_') and not callable(getattr(obj, attr)) and attr not in ['metadata', 'registry', 'load_options', 'statement', 'selectable', 'is_single_entity', 'get_label_style', 'whereclause', 'lazy_loaded_from', 'column_descriptions', 'logger', 'dispatch']]

  '''List returns each corresponding value for SQLattrs'''
  def List(obj):
    print(InfoGet.SQLattrs(obj))
    return [obj.__dict__[i] for i in InfoGet.SQLattrs(obj)]
  
  def ListCensor(obj, admin=0):
    k = []
    m = InfoGet.SQLattrs(obj)
    traits = {}
    print(type(obj), list(ALJ.keys()))
    if obj.__class__.__name__ in ALJ.keys():
      print("HELLLO")
      traits = ALJ[obj.__class__.__name__]
      print(f"\n\n\n\n{admin}\n\n\n\n")
    for i in m:
      if i in traits.keys() and int(traits[i]) < int(admin):
        k.append("Hidden")
      else:
        k.append(obj.__dict__[i])
    return k

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
      else:
        stringy.append("HIDDEN")
        stringy.append("HIDDEN")
        stringy.append("HIDDEN")
      if admin_level > 1:
        stringy.append(element.national_id)
      else:
        stringy.append("HIDDEN")
      if admin_level > 2:
        gooner = session.query(Bank).filter_by(national_id=element.national_id).first()
        stringy.append(gooner.woolong)
        stringy.append(gooner.parts)
        stringy.append(gooner.credit)
      else:
        stringy.append("HIDDEN")
        stringy.append("HIDDEN")
        stringy.append("HIDDEN")
      database_list.append(stringy)
    return database_list

  #make this dependent on admin level!
  def getMail(userid):
    outlist = []
    for k in session.query(Mail).all():
      if k.acc_id_to == userid:
        outlist.append([k.title,k.message,k.contact if k.contact else None])
    return outlist
    
  #Collects reports based on the admin's level
  def reportCollect(admin_level, reports):
    database_list = []
    for element in reports:
      stringy = [element.id]
      if admin_level > 3:
        stringy.append(element.woolong)
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
    database_list = []
    for element in accs:
      stringy = []
      print(element.national_id)
      stringy.append(element.woolong)
      stringy.append(element.parts)
      stringy.append(element.credit)
      database_list.append(stringy)
    return database_list
