from hfc.fabric import Client as client_fabric
from flask import *
from tornado.platform.asyncio import AnyThreadEventLoopPolicy
from vininfo import Vin
from concurrent.futures import ThreadPoolExecutor
import asyncio, couchdb, json, random, multiprocessing, os, js2py

domain = "ptb.de"
channel_name = "nmi-channel"
cc_name = "fabpki"
cc_version = "1.0"

app = Flask(__name__)

asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())  

class ThreadingFunction:
    def ProcessModelo(id, arq_json):
        loop = asyncio.get_event_loop()

        c_hlf = client_fabric(net_profile=(domain + ".json"))

        admin = c_hlf.get_user(domain, 'Admin')
        
        callpeer = "peer0." + domain
        
        c_hlf.new_channel(channel_name)

        response = loop.run_until_complete(c_hlf.chaincode_invoke(
            requestor=admin, 
            channel_name=channel_name, 
            peers=[callpeer],
            cc_name=cc_name, 
            cc_version=cc_version,
            fcn='registrarModeloPBE', 
            args=[id, arq_json[id]["Categoria"], arq_json[id]["Fabricante"].upper(), arq_json[id]["Versao"], arq_json[id]["Modelo"], str(arq_json[id]["Emissao"])], 
            cc_pattern=None))

    def ProcessPlaca():
        
        exe = ThreadPoolExecutor(max_workers=5)
        listPlacas = []
        listModelos = [] 
        listLetras = []
        listNums = []
        
        with open('pbe-veicular.json') as f:
            arq_json = json.load(f)

        def getModelos(modelo):
            listModelos.append(modelo)
            
        def getLetter():
            letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
            'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            letter = random.choice(letras)
            listLetras.append(letter)
                
        def getNum():
            nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            num = random.choice(nums)
            listNums.append(str(num))

        def makePlaca():

            for l in range(4):
                t = exe.submit(getLetter)
                
            for n in range(3):
                t = exe.submit(getNum)
                
            while len(listLetras) != 4:
                pass
            while len(listNums) != 3:
                pass
            
            placa = listLetras[0] + listLetras[1] + listLetras[2] + listNums[0] + listLetras[3] + listNums[1] + listNums[2]
            
            listPlacas.append(placa)
            
        for m in arq_json:
            t = exe.submit(getModelos(m))
            
        t = exe.submit(makePlaca)

        while len(listPlacas) != 1:
            pass
        
        loop = asyncio.get_event_loop()

        c_hlf = client_fabric(net_profile=(domain + ".json"))

        admin = c_hlf.get_user(domain, 'Admin')
        
        callpeer = "peer0." + domain
        
        c_hlf.new_channel(channel_name)
            
        response = loop.run_until_complete(
            c_hlf.chaincode_invoke(requestor=admin,
                                channel_name=channel_name,
                                peers=[callpeer],                               
                                args=[listPlacas[0], ('model-' + (random.choice(listModelos)))],
                                cc_name=cc_name,
                                cc_version=cc_version,
                                fcn='registrarVeiculoPBE',
                                cc_pattern=None))
        
    def processarTrajeto(idVeiculo):
        
        distancia = random.randrange(0, 250)
        loop = asyncio.get_event_loop()

        c_hlf = client_fabric(net_profile=(domain + ".json"))

        admin = c_hlf.get_user(domain, 'Admin')
        
        callpeer = "peer0." + domain
        
        c_hlf.new_channel(channel_name)
        
        response = loop.run_until_complete(
            c_hlf.chaincode_invoke(requestor=admin,
                                channel_name=channel_name,
                                peers=[callpeer],                               
                                args=[],
                                cc_name=cc_name,
                                cc_version=cc_version,
                                fcn='registrarVeiculoPBE',
                                cc_pattern=None))
                    

@app.route('/modeloPBE', methods=['POST', 'GET'])
def Modelo():
    if request.method == 'GET':
        listaModelos = []
        server = couchdb.Server('http://localhost:5984/_utils')
        couch = couchdb.Server()
        db = couch['nmi-channel_fabpki']
        
        for doc in db.view('_all_docs'):
                i = doc['id']
                if i[0:6] == "model-":
                    for doc in db.find({
                            "selector": {
                            "_id": "{id}".format(id=i)
                            }}):
                            query_info = json.dumps(doc, indent=4, sort_keys=True)
                            query_json = json.loads(query_info)
                            infoModelo = query_json
                            listaModelos.append(infoModelo)
                    
        return json.dumps(listaModelos), 200    

    if request.method == 'POST':

        with open('pbe-veicular.json') as f:
            arq_json = json.load(f)
        
        pool = multiprocessing.Pool(processes=os.cpu_count())
        processes = [pool.apply_async(ThreadingFunction.ProcessModelo, args=(k, arq_json,)) for k in arq_json]
        
        return Response(response=json.dumps({
            "status": 201,
            "mensagem": "Modelos do PBE registrados com sucesso"}), status=201, mimetype='application/json')

@app.route('/fabricante', methods=['POST', 'GET'])
def Fabricante():
    if request.method == 'GET':
        listaFabricantes = []
        server = couchdb.Server('http://localhost:5984/_utils')
        couch = couchdb.Server()
        db = couch['nmi-channel_fabpki']
        
        for doc in db.view('_all_docs'):
                i = doc['id']
                if i[0:4] == "fab-":
                    for doc in db.find({
                            "selector": {
                            "_id": "{id}".format(id=i)
                            }}):
                            query_info = json.dumps(doc, indent=4, sort_keys=True)
                            query_json = json.loads(query_info)
                            infoVeiculo = query_json
                            listaFabricantes.append(infoVeiculo)
                    
        return json.dumps(listaFabricantes), 200    
    
    if request.method == 'POST':
        
        request_data = request.get_json()

        loop = asyncio.get_event_loop()

        c_hlf = client_fabric(net_profile=(domain + ".json"))

        admin = c_hlf.get_user(domain, 'Admin')
        
        callpeer = "peer0." + domain
        
        c_hlf.new_channel(channel_name)
        
        fab_nome = request_data["nome"]

        response = loop.run_until_complete(
            c_hlf.chaincode_invoke(requestor=admin,
                                channel_name=channel_name,
                                peers=[callpeer],                               
                                args=[fab_nome.upper()],
                                cc_name=cc_name,
                                cc_version=cc_version,
                                fcn='registrarFabricante',
                                cc_pattern=None))
        
        return Response(response=json.dumps({
            "status": 201,
            "mensagem": "Fabricante registrado com sucesso"}), status=201, mimetype='application/json')
    
@app.route('/veiculo', methods=['GET', 'POST'])
def Veiculo():
    if request.method == 'GET':
        listaVeiculos = []
        server = couchdb.Server('http://localhost:5984/_utils')
        couch = couchdb.Server()
        db = couch['nmi-channel_fabpki']
        
        for doc in db.view('_all_docs'):
                i = doc['id']
                if i[0:5] == "veic-":
                    for doc in db.find({
                            "selector": {
                            "_id": "{id}".format(id=i)
                            }}):
                            query_info = json.dumps(doc, indent=4, sort_keys=True)
                            query_json = json.loads(query_info)
                            infoVeiculo = query_json
                            listaVeiculos.append(infoVeiculo)
                    
        return json.dumps(listaVeiculos), 200
    
    if request.method == 'POST':
        
        WMI = [['93G', 'KAWASAKI'], ['932', 'HARLEY-DAVIDSON'], ['9CD', 'SUZUKI'], ['93W', 'FIAT DUCATO'], ['9BM', 'MERCEDES-BENZ'], ['94T', 'TROLLER'], ['936', 'PEUGEOT'], ['935', 'CITROEN'], ['94D', 'NISSAN'], ['93Y', 'RENAULT'], ['93X', 'MITSUBISH'], ['93U', 'AUDI'], ['93H', 'HONDA'], ['9BR', 'TOYOTA'], ['9BD', 'FIAT'], ['9BF', 'FORD'], ['9BG', 'CHEVROLET'], ['9BW', 'VOLKSWAGEN'], ['93R', 'TOYOTA']]
        
        
        request_data = request.get_json()
        
        loop = asyncio.get_event_loop()

        c_hlf = client_fabric(net_profile=(domain + ".json"))

        admin = c_hlf.get_user(domain, 'Admin')
        
        callpeer = "peer0." + domain
        
        c_hlf.new_channel(channel_name)
        
        fabNome = ''        
        vin = request_data["Vin"]
        try:
            vinType = Vin(vin)
            fabNome = (vinType.manufacturer).upper().replace(" ", "")
        except:
            for i in WMI:
                if vin[0:3] == i[0]:
                    fabNome = i[1]
                    break
            pass
            
    
        response = loop.run_until_complete(
            c_hlf.chaincode_invoke(requestor=admin,
                                channel_name=channel_name,
                                peers=[callpeer],                               
                                args=[vin, request_data["Hash"], request_data["Co2"], fabNome],
                                cc_name=cc_name,
                                cc_version=cc_version,
                                fcn='registrarVeiculo',
                                cc_pattern=None))
        
        return Response(response=json.dumps({
            "status": 201,
            "mensagem": "Veiculo registrado com sucesso"}), status=201, mimetype='application/json')

@app.route('/veiculoPBE', methods=['POST'])
def VeiculoPBE():
    
    if request.method == 'POST':

        pool = multiprocessing.Pool(processes=os.cpu_count())
        processes = [pool.apply_async(ThreadingFunction.ProcessPlaca,) for p in range(1000)]
        
        return Response(response=json.dumps({
            "status": 201,
            "mensagem": "Saldo dos fabricantes atualizados com suceso"}), status=201, mimetype='application/json')        

@app.route('/saldo', methods=['POST'])
def Saldo():
    if request.method == 'POST':
        listaVeiculos = []
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
                if i[0:4] == "fab-":
                    listaVeiculos.append(i)
        
        for i in listaVeiculos:
            response = loop.run_until_complete(
                c_hlf.chaincode_invoke(requestor=admin,
                                    channel_name=channel_name,
                                    peers=[callpeer],                               
                                    args=[i],
                                    cc_name=cc_name,
                                    cc_version=cc_version,
                                    fcn='registrarCredito',
                                    cc_pattern=None))
            
        return Response(response=json.dumps({
            "status": 201,
            "mensagem": "Saldo dos fabricantes atualizados com suceso"}), status=201, mimetype='application/json')
            

@app.route('/ordem', methods=['GET', 'POST'])
def Ordem():
    if request.method == 'GET':
        listaTransacoes = []
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
                            infoVeiculo = query_json
                            listaTransacoes.append(infoVeiculo)
                    
        return json.dumps(listaTransacoes), 200

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
                                args=[request_data["ProprietarioOrdem"], request_data["TipoTransacao"], request_data["SaldoOfertado"]],
                                cc_name=cc_name,
                                cc_version=cc_version,
                                fcn='anunciarOrdem',
                                cc_pattern=None))
        
        return Response(response=json.dumps({
            "status": 201,
            "mensagem": "Ordem de transação registrada com sucesso"}), status=201, mimetype='application/json')    

@app.route('/lance', methods=['POST'])
def Lance():
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
                                args=[request_data["IdTransacao"], request_data["ValorLance"], request_data["IdComprador"]],
                                cc_name=cc_name,
                                cc_version=cc_version,
                                fcn='ordemLance',
                                cc_pattern=None))
        
        return Response(response=json.dumps({
            "status": 201,
            "mensagem": "Lance registradao com sucesso"}), status=201, mimetype='application/json')    

@app.route('/fechar_ordem', methods=['POST'])
def FecharOrdem():
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
                                args=[request_data["IdTransacao"], request_data["IdProprietario"]],
                                cc_name=cc_name,
                                cc_version=cc_version,
                                fcn='fecharOrdem',
                                cc_pattern=None))
        
        return Response(response=json.dumps({
            "status": 201,
            "mensagem": "Lance registradao com sucesso"}), status=201, mimetype='application/json') 
    
if __name__ == "__main__":
    app.run(debug=True, port=8001, host="0.0.0.0")
