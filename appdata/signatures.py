#signatures.py

from appdata.database import Base, engine, DATABASE_URL, start_session
from appdata.models import Signature
import random, datetime
session = start_session()
SMAL = 1
LARG = 10**50
class LoginSignatures:
    def createSignature(national_id, autocommit=True):
        random.seed(str(datetime.datetime.now()) + str(national_id))
        k = random.randrange(SMAL, LARG)
        new_signature = Signature(signature=str(k), national_id=national_id)
        if autocommit:
            session.add(new_signature)
            session.commit()
        return new_signature

    def deleteSignature(signature):
        k = session.query(Signature).filter_by(signature=signature).first()
        if k:
            session.delete(k)
            session.commit()
            return None
        else:
            return "Signature doesn't exist!"

    def deleteAllSignatures():
        for i in session.query(Signature).all():
            session.delete(i)
            session.commit()
        return None
