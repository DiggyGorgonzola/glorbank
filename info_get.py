# info_get.py

# This is a completely new system. Might not work!
class InfoGet():
  def admin_info_collect(self, admin_level):
    database_list = []
    for element in session.query(User).all():
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
      if admin_level > 2:
        print(element.national_id)
        gooner = session.query(Bank).filter_by(national_id=element.national_id).first()
        stringy.append(gooner.bank_value)
      else:
        stringy.append("HIDDEN")
      database_list.append(stringy)
    return database_list
    
  #Collects reports based on the admin's level
  def admin_reports_collect(self, admin_level):
    database_list = []
    for element in session.query(Reports).all():
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
      # FINISH???
  
  def admin_pending_orgs_collect(self, admin_level):
    database_list = []
    for element in session.query(RegisteringOrganizations).all():
      stringy = [element.id, element.accdate, element.name, element.email, element.phone]
      database_list.append(stringy)
  return database_list
