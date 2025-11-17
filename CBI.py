#CBI.py
import datetime

# MAIN BANK VARIABLES
# ---------
suspicious_transaction_limit = 100 # If a transaction occurs above this limit, then the user will have to wait for a banker to verify the transaction
woolong_to_diamond = 5 # Woolong to diamond static conversion rate
woolong_to_parts = 0.05 # Woolong to parts static conversion rate
woolong_to_usd = 0 # Woolong to USD static conversion rate
woolong_value_in_reserves = 0 #The number of Woolong in the bank reserves that can be given to bank accounts 
debug = [True, True] # DEBUG = (<allow print statements>, <allow sensitive print statements>)
cbidict = {"suspicious_transaction_limit": suspicious_transaction_limit,
           "woolong_to_diamond": woolong_to_diamond,
           "woolong_to_parts": woolong_to_parts,
           "woolong_to_usd": woolong_to_usd,
           "woolong_value_in_reserves": woolong_value_in_reserves,
           "debug": debug
}
# ---------





# HIDDEN BANK VARIABLES
# ---------
LOCKDOWN = False # Basically freezes the bank entirely
SECRETKEY = "GINGINATOR3000" # Secret ID key for changing variables (Do not keep it GINGINATOR3000 for the real app. People can see this github page
HISTORY = [] # Variable change history
CHANGEVALUEALLOW = False # Allow bank values to be changed
HOMEREDIRECT = "register.html"
# ---------



# CHANGE BANK VALUES
# ---------
# may not be needed depending on the hosting service.
def changeValue(variable_id_change, variable_change, identification_code):
  current_time = datetime.datetime.now()
  if identification_code != SECRETKEY and not LOCKDOWN:
    LOCKDOWN = True
  elif CHANGEVALUEALLOW:
    if variable_id_change in cbidict.keys():
      cbidict[variable_id_change] = variable_id_change
    ''' ALTERNATIVELY:
    if variable_id_change in globals():
      globals()[variable_id_change] = variable_change
    '''
    HISTORY.append(f"{current_time}|variable id change: {variable_id_change}|variable change {variable_change}")
# ---------

#I'm not sure if this will really be used. But it may be nice to have...
# It will be used to hold all the bank info that we dont want anybody to be able to change. If someone does change it, it may spell disaster!
