
class InfoGet():
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
      if admin_level > 1:
        stringy.append(element.national_id)
      else:
        stringy.append("HIDDEN")
      else:
        stringy.append("HIDDEN")
        stringy.append("HIDDEN")
        stringy.append("HIDDEN")
      database_list.append(stringy)
    return database_list
    
  #Collects reports based on the admin's level
  def reportCollect(admin_level, reports):
    database_list = []
    for element in reports:
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
  
  def pendOrgCollect(admin_level, orgs):
    database_list = []
    for element in orgs:
      stringy = [element.id, element.accdate, element.name, element.email, element.phone]
      database_list.append(stringy)
    return database_list
  
  def bankCollect(admin_level, accs):
    stringy = []
    for element in accs:
      print(element.national_id)
      stringy.append(element.woolong)
      stringy.append(element.parts)
      stringy.append(element.credit)
      database_list.append(stringy)
    return database_list
      
    
