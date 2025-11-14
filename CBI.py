#CBI.py
suspicious_transaction_limit = 100
woolong_to_diamond = 5
woolong_to_parts = 0.05
woolong_to_usd = 0
woolong_value_in_reserves = 0
LOCKDOWN = False
SECRETKEY = "GINGINATOR3000"
HISTORY = []

CHANGEVALUEALLOW = False
# may not be needed depending on the hosting service.
def changeValue(variable_id_change, variable_change, identification_code):
  current_time = datetime.datetime.now()
  if identification_code != SECRETKEY and not LOCKDOWN:
    LOCKDOWN = True
  elif CHANGEVALUEALLOW:
    if variable_id_change == 0:
      suspicious_transaction_limit = variable_change
    elif variable_id_change == 1:
      woolong_to_diamond = variable_change
    elif variable_id_change == 2:
      woolong_to_parts = variable_change
    elif variable_id_change == 3:
      woolong_to_usd = variable_change
    elif variable_id_change == 4:
      woolong_value_in_reserves = variable_change
    HISTORY.append(f"{current_time}|variable id change: {variable_id_change}|variable change {variable_change}")
  

#I'm not sure if this will really be used. But it may be nice to have...
# It will be used to hold all the bank info that we dont want anybody to be able to change. If someone does change it, it may spell disaster!
