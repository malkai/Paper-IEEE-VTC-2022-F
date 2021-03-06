import firebase_admin 
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db


#this function insert data on database
def insertele(vehicle):

	connect_fire = firestore.client()
	connect_fire.collection(u'Teste').document(u'carros').add(vehicle.to_dict())
	connect_fire.close()

#this function get data on database
def getDoc():

	connect_fire = firestore.client()
	
	usersref = connect_fire.collection(u'dataPoints').where('isAccounted', '==', False)
	docs = usersref.stream()
	return docs

def change_flag(y):
	connect_fire = firestore.client()
	a = True
	for doc in y:
			
			city_ref = connect_fire.collection(u'dataPoints').document(getattr(doc,'hash'))
			city_ref.update(
			{
    				'isAccounted': True
			})
    		
#this two lines setup credential on Database
cred_obj = firebase_admin.credentials.Certificate('.env/paper-ieee-vtc-2022-firebase-adminsdk-t36ql-4f5d60dca7.json')
default_app = firebase_admin.initialize_app(cred_obj)