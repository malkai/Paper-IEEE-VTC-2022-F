import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def insertele(vehicle):

	db = firestore.client()
	db.collection(u'Teste').document(u'carros').add(vehicle.to_dict())
	db.close()

cred_obj = firebase_admin.credentials.Certificate('.env/paper-ieee-vtc-2022-firebase-adminsdk-t36ql-4f5d60dca7.json')
default_app = firebase_admin.initialize_app(cred_obj)