from hfc.fabric import Client as client_fabric
from flask import *
from tornado.platform.asyncio import AnyThreadEventLoopPolicy
from vininfo import Vin
import asyncio, couchdb, json

domain = "ptb.de"
channel_name = "nmi-channel"
cc_name = "fabpki"
cc_version = "1.0"

app = Flask(__name__)

asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())    

@app.route('/manufacturer', methods=['POST', 'GET'])
def manufacturer():
    if request.method == 'GET':
        listaManufacturers = []
        server = couchdb.Server('http://localhost:5984/_utils')
        couch = couchdb.Server()
        db = couch['nmi-channel_fabpki']
        
        for doc in db.view('_all_docs'):
                i = doc['id']
                if i[0:5] == "manu-":
                    for doc in db.find({
                            "selector": {
                            "_id": "{id}".format(id=i)
                            }}):
                            query_info = json.dumps(doc, indent=4, sort_keys=True)
                            query_json = json.loads(query_info)
                            infoVehicle = query_json
                            listaManufacturers.append(infoVehicle)
                    
        return json.dumps(listaManufacturers), 200    
    
    if request.method == 'POST':
        
        request_data = request.get_json()

        loop = asyncio.get_event_loop()

        c_hlf = client_fabric(net_profile=(domain + ".json"))

        admin = c_hlf.get_user(domain, 'Admin')
        
        callpeer = "peer0." + domain
        
        c_hlf.new_channel(channel_name)
        
        fab_nome = request_data["name"]

        response = loop.run_until_complete(
            c_hlf.chaincode_invoke(requestor=admin,
                                channel_name=channel_name,
                                peers=[callpeer],                               
                                args=[fab_nome.upper()],
                                cc_name=cc_name,
                                cc_version=cc_version,
                                fcn='registerManufacturer',
                                cc_pattern=None))
        
        return Response(response=json.dumps({
            "status": 201,
            "message": "manufacturer successfully registered"}), status=201, mimetype='application/json')
    
@app.route('/vehicle', methods=['GET', 'POST'])
def vehicle():
    if request.method == 'GET':
        listVehicles = []
        server = couchdb.Server('http://localhost:5984/_utils')
        couch = couchdb.Server()
        db = couch['nmi-channel_fabpki']
        
        for doc in db.view('_all_docs'):
                i = doc['id']
                if i[0:5] == "vehi-":
                    for doc in db.find({
                            "selector": {
                            "_id": "{id}".format(id=i)
                            }}):
                            query_info = json.dumps(doc, indent=4, sort_keys=True)
                            query_json = json.loads(query_info)
                            infovehicle = query_json
                            listVehicles.append(infovehicle)
                    
        return json.dumps(listVehicles), 200
    
    if request.method == 'POST':
        
        request_data = request.get_json()
        
        loop = asyncio.get_event_loop()

        c_hlf = client_fabric(net_profile=(domain + ".json"))

        admin = c_hlf.get_user(domain, 'Admin')
        
        callpeer = "peer0." + domain
        
        c_hlf.new_channel(channel_name)
        
        WMI = [['93G', 'KAWASAKI'], ['932', 'HARLEY-DAVIDSON'], ['9CD', 'SUZUKI'], ['93W', 'FIAT DUCATO'], ['9BM', 'MERCEDES-BENZ'], ['94T', 'TROLLER'], ['936', 'PEUGEOT'], ['935', 'CITROEN'], ['94D', 'NISSAN'], ['93Y', 'RENAULT'], ['93X', 'MITSUBISH'], ['93U', 'AUDI'], ['93H', 'HONDA'], ['9BR', 'TOYOTA'], ['9BD', 'FIAT'], ['9BF', 'FORD'], ['9BG', 'CHEVROLET'], ['9BW', 'VOLKSWAGEN'], ['93R', 'TOYOTA']]

        ManuName = ''        
        vin = request_data["Vin"]
        try:
            vinType = Vin(vin)
            ManuName = (vinType.manufacturer).upper().replace(" ", "")
        except:
            for i in WMI:
                if vin[0:3] == i[0]:
                    ManuName = i[1]
                    break
            pass

        response = loop.run_until_complete(
            c_hlf.chaincode_invoke(requestor=admin,
                                channel_name=channel_name,
                                peers=[callpeer],                               
                                args=[vin, request_data["Hash"], request_data["Co2"], ManuName],
                                cc_name=cc_name,
                                cc_version=cc_version,
                                fcn='registerVehicle',
                                cc_pattern=None))
        
        return Response(response=json.dumps({
            "status": 201,
            "message": "Vehicle registered successfully"}), status=201, mimetype='application/json')

@app.route('/babid', methods=['POST'])
def babid():
    if request.method == 'POST':
        listVehicles = []
        server = couchdb.Server('http://localhost:5984/_utils')
        couch = couchdb.Server()
        db = couch['nmi-channel_fabpki']
        loop = asyncio.get_event_loop()
        c_hlf = client_fabric(net_profile=(domain + ".json"))
        admin = c_hlf.get_user(domain, 'Admin')
        callpeer = "peer0." + domain
        c_hlf.new_channel(channel_name)
        
        for doc in db.view('_all_docs'):
                i = doc['id']
                if i[0:5] == "manu-":
                    listVehicles.append(i)
        
        for i in listVehicles:
            response = loop.run_until_complete(
                c_hlf.chaincode_invoke(requestor=admin,
                                    channel_name=channel_name,
                                    peers=[callpeer],                               
                                    args=[i],
                                    cc_name=cc_name,
                                    cc_version=cc_version,
                                    fcn='registerCredit',
                                    cc_pattern=None))
            
        return Response(response=json.dumps({
            "status": 201,
            "message": "manufacturers babid updated successfully"}), status=201, mimetype='application/json')
            

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'GET':
        listTransactions = []
        server = couchdb.Server('http://localhost:5984/_utils')
        couch = couchdb.Server()
        db = couch['nmi-channel_fabpki']
        
        for doc in db.view('_all_docs'):
                i = doc['id']
                if i[0:6] == "trans-":
                    for doc in db.find({
                            "selector": {
                            "_id": "{id}".format(id=i)
                            }}):
                            query_info = json.dumps(doc, indent=4, sort_keys=True)
                            query_json = json.loads(query_info)
                            infovehicle = query_json
                            listTransactions.append(infovehicle)
                    
        return json.dumps(listTransactions), 200

    if request.method == 'POST' :
      
        request_data = request.get_json()
        
        loop = asyncio.get_event_loop()

        c_hlf = client_fabric(net_profile=(domain + ".json"))

        admin = c_hlf.get_user(domain, 'Admin')
        
        callpeer = "peer0." + domain
        
        c_hlf.new_channel(channel_name)

        response = loop.run_until_complete(
            c_hlf.chaincode_invoke(requestor=admin,
                                channel_name=channel_name,
                                peers=[callpeer],                               
                                args=[request_data["orderOwner"], request_data["transactionType"], request_data["offeredBabid"]],
                                cc_name=cc_name,
                                cc_version=cc_version,
                                fcn='announceOrder',
                                cc_pattern=None))
        
        return Response(response=json.dumps({
            "status": 201,
            "message": "order transaction successfully registered"}), status=201, mimetype='application/json')    

@app.route('/bid', methods=['POST'])
def bid():
    if request.method == 'POST' :
        
        request_data = request.get_json()
        
        loop = asyncio.get_event_loop()

        c_hlf = client_fabric(net_profile=(domain + ".json"))

        admin = c_hlf.get_user(domain, 'Admin')
        
        callpeer = "peer0." + domain
        
        c_hlf.new_channel(channel_name)

        response = loop.run_until_complete(
            c_hlf.chaincode_invoke(requestor=admin,
                                channel_name=channel_name,
                                peers=[callpeer],                               
                                args=[request_data["transactionId"], request_data["valueBid"], request_data["buyerId"]],
                                cc_name=cc_name,
                                cc_version=cc_version,
                                fcn='bidOrder',
                                cc_pattern=None))
        
        return Response(response=json.dumps({
            "status": 201,
            "message": "bid successfully registered"}), status=201, mimetype='application/json')    

@app.route('/closeOrder', methods=['POST'])
def closeOrder():
    if request.method == 'POST' :
        
        request_data = request.get_json()
        
        loop = asyncio.get_event_loop()

        c_hlf = client_fabric(net_profile=(domain + ".json"))

        admin = c_hlf.get_user(domain, 'Admin')
        
        callpeer = "peer0." + domain
        
        c_hlf.new_channel(channel_name)

        response = loop.run_until_complete(
            c_hlf.chaincode_invoke(requestor=admin,
                                channel_name=channel_name,
                                peers=[callpeer],                               
                                args=[request_data["idTransaction"], request_data["idOwner"]],
                                cc_name=cc_name,
                                cc_version=cc_version,
                                fcn='closeOrder',
                                cc_pattern=None))
        
        return Response(response=json.dumps({
            "status": 201,
            "message": "Order successfully closed"}), status=201, mimetype='application/json') 
    
if __name__ == "__main__":
    app.run(debug=True, port=8001, host="0.0.0.0")