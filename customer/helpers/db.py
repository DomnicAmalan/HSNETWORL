import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# cred = credentials.ApplicationDefault()
# firebase_admin.initialize_app(cred, {
#   'projectId': ,
# })


cred = credentials.Certificate(os.path.join('', 'customer/static/cred.json'))
firebase_admin.initialize_app(cred)

db = firestore.client()
