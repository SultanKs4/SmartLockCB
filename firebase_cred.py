import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('YOUR_CREDENTIALS')
firebase_admin.initialize_app(cred)
firestore_db = firestore.client()
smart_lock_col = firestore_db.collection(u'YOUR_COLLECTION')


