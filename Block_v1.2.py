import json
import hashlib
import datetime
from urllib.parse import urlparse
import flask
from flask import Flask, jsonify, request, render_template
import requests

class Block:
    def __init__(self, index, red_id, transacciones, tiempo, hash_previo):
        self.index = index
        self.red_id = red_id
        self.transacciones = transacciones
        self.tiempo = tiempo
        self.hash_previo = hash_previo
        self.nonce = 0

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    dificultad = 4

    def __init__(self):
        self.transacciones_sin_confirmar = []
        self.chain = []
        self.create_genesis_block()
        self.nodos = set()


    def to_dict(self):
        chain_dict = []
        for block in self.chain:
            block_dict = {
                "index": block.index,
                "red_id": block.red_id,
                "tiempo": block.tiempo,
                "hash_previo": block.hash_previo,
                "hash": block.hash,
                "nonce": block.nonce,
                "transacciones": block.transacciones
            }
            chain_dict.append(block_dict)
        #return {"chain": chain_dict}
        return {"Longitud de la Cadena": len(self.chain),
                "cadena": chain_dict}

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodos.add(parsed_url.netloc)

    def proof_of_work_genesis(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.dificultad):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash, block.nonce

    def create_genesis_block(self):
        genesis_block = Block(0, "Red_Tangle_X", ["Bloque Genesis"], str(datetime.datetime.now()), "0" * 64)
        genesis_block.hash, genesis_block.nonce = self.proof_of_work_genesis(genesis_block)
        self.chain.append(genesis_block)

    def get_block_by_id(self, block_id):
        for block in self.chain:
            if block.index == block_id:
                return block
        return None

    @property
    def last_block(self):
        return self.chain[-1]

    def print_block(self, n):
        if len(self.chain) < n:
            return
        else:
            block = self.chain[n]
            return "\nIndex: {}\nID_red: {}\nTransacciones: {}\nTiempo: {}\nHash_Previo: {}\nHash: {}\nNonce: {}\n".format(
                block.index, block.red_id, block.transacciones, block.tiempo, block.hash_previo, block.hash, block.nonce
            )

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.dificultad):
            block.nonce += 1
            computed_hash = block.compute_hash()
        print(f'Computed hash: {computed_hash}')
        expected_hash = self.is_valid_proof(block, computed_hash)
        print(f'Expected hash: {expected_hash}')
        return computed_hash

    def add_block(self, block, proof):
        hash_previo = self.last_block.hash
        if hash_previo != block.hash_previo:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        return (int(block_hash, 16) < 2 ** (256 - Blockchain.dificultad) and block_hash == block.compute_hash())

    def add_new_transaction(self, transaction):
        self.transacciones_sin_confirmar.append(transaction)

    def mine(self, red_id):
        if not self.transacciones_sin_confirmar:
            return False
        last_block = self.last_block
        new_block = Block(
            index=last_block.index + 1,
            red_id=red_id,
            transacciones=self.transacciones_sin_confirmar,
            tiempo=str(datetime.datetime.now()),
            hash_previo=last_block.hash
        )
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.transacciones_sin_confirmar = []
        return new_block.index

    def is_valid_chain(self, cadena):
        if isinstance(cadena, str):
            cadena = json.loads(cadena)
        for i in range(1, len(cadena)):
            block = cadena[i]
            prev_block = cadena[i - 1]
            if block["hash_previo"] != prev_block["hash"]:
                print(f'Block {i} previous hash mismatch: {block["hash_previo"]} != {prev_block["hash"]}')
                return False
        return True

    def consenso(self):
        if len(blockchain.nodos)<1:
            return False
        else:
            vecinos = self.nodos
            nueva_cadena = None

            # Busca una cadena más larga que la nuestra
            longitud_maxima = len(self.chain)
            print(longitud_maxima)
            for nodo in vecinos:
                response = requests.get(f'http://{nodo}/chain2')
                if response.status_code == 200:
                    longitud = response.json()['Longitud de la Cadena']
                    cadena = response.json()['cadena']
                    print(longitud)
                    print(cadena)
                    print(blockchain.is_valid_chain(cadena))
                    # Comprueba si la longitud es mayor y la cadena es válida

                    if longitud > longitud_maxima and blockchain.is_valid_chain(cadena):
                        longitud_maxima = longitud
                        nueva_cadena = cadena
                        print("Si es valida")

            # Reemplaza nuestra cadena si encontramos una más larga y válida
            if nueva_cadena:
                print("Se llegó hasta aquí")
                new_chain = []
                for block_data in nueva_cadena:
                    block = Block(
                        index=block_data["index"],
                        red_id=block_data["red_id"],
                        transacciones=block_data["transacciones"],
                        tiempo=block_data["tiempo"],
                        hash_previo=block_data["hash_previo"]
                    )
                    block.hash = block_data["hash"]
                    block.nonce = block_data["nonce"]
                    new_chain.append(block)
                self.chain = new_chain
                return True
            return False

# Crear una instancia de la clase Blockchain
blockchain = Blockchain()

blockchain.add_node("http://192.168.0.107:5000")
blockchain.add_node("http://192.168.0.112:5000")


#Crear transacciones
#blockchain.add_new_transaction('S1:Temp:51')
#blockchain.add_new_transaction('S1:Hum:15')
#blockchain.add_new_transaction('S2:Temp:33')
#blockchain.add_new_transaction('S2:Hum:42')
#minar el bloque - Definir quien crea la red
#blockchain.mine('Red_Tangle_A')
##Impimir la blockchain en consola
#tam=len(blockchain.chain)
#for x in range(tam):
#    print(blockchain.print_block(x))
##Comprobar que la cadena sea valida
#aa=blockchain.to_json()
#print(aa)
#cadena = json.loads(aa)["cadena"]
#print(cadena)
#print(blockchain.is_valid_chain(cadena))
##Consenso para verificar demas blockchains
#print(blockchain.consenso())
##Agregamos 1 nodo
#blockchain.add_node("http://192.168.0.107:5000")
#blockchain.add_node("http://192.168.0.112:5000")
#blockchain.add_node("http://172.20.131.189:5000")
#print(blockchain.nodos)
##Consenso x2 con el nodo
#print(blockchain.consenso())

app = Flask(__name__)

@app.route('/')
def index():
    #Impimir la blockchain en consola
    tam = len(blockchain.chain)
    for x in range(tam):
        print(blockchain.print_block(x))
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return render_template('index.html', data=chain_data)


@app.route('/block/<int:block_id>')
def block_detail(block_id):
    block = blockchain.get_block_by_id(block_id)
    return render_template('block_detail.html', block=block)

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [{"Longitud de la Cadena": len(blockchain.chain)}]
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return flask.jsonify(chain_data)

@app.route('/chain2', methods=['GET'])
def get_chain2():
    return blockchain.to_json()

@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    requiere_fields = ["Nodo", "sensorPH", "sensorTEMP"]
    for field in requiere_fields:
        if not tx_data.get(field):
            return "Datos de transaccion invalidos", 404
    tx_data["tiempo"] = str(datetime.datetime.now())
    blockchain.add_new_transaction(tx_data)
    return "Exito¡¡, transaccion agregada", 201
#######################################################################################################
@app.route('/mine', methods=['GET'])
def mine_unconfirmated_transactions():
    ID_redtangle = 'Red Tangle A -- 192.168.0.104 - ISLA 1'      ## cambiar dependiendo del nodo---------------------------
    result=blockchain.mine(ID_redtangle)
    vecinos=blockchain.nodos
    if not result:
        return "Nada que minar"
    for nodo in vecinos:
        response = requests.get(f'http://{nodo}/consenso')
        if response.status_code == 200:
            print("Se ha llamado al Consenso de todos los Nodos")
    return "El bloque #{} es minado y se ha llamado al Consenso de los demás nodos".format(result)
#######################################################################################################
@app.route('/transacciones_pendientes', methods=['GET'])
def get_pending_tx():
    return json.dumps(blockchain.transacciones_sin_confirmar)

#conectando nuevos nodos
@app.route('/conectar_nodos', methods=['POST'])
def conectar_nodos():
    json = request.get_json()
    nodos = json.get('nodos')
    if nodos is None:
        return "Ningun Nodo", 401
    for nodos in nodos:
        blockchain.add_node(nodos)
    response ={'message': 'Todos los nodos estan ahora conectados. Se contiene los siguientes nodos',
               'total_nodes':list(blockchain.nodos)}
    return jsonify(response), 201

@app.route('/nodos', methods=['GET'])
def nodos():
    cant_nodos=len(blockchain.nodos)
    response = {'Cantidad de Nodos': cant_nodos,
                'Nodos': list(blockchain.nodos)}
    return jsonify(response), 200

#remplazando la cadena por la más larga
@app.route('/consenso', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.consenso()
    if is_chain_replaced:
        response = {'message':'los nodos tenian diferentes cadenas asi que la cadena fue remplazada por la más larga',
                    'new_chain': blockchain.to_json()}
    else:
        response = {'message':'Todo bien la cadena es la más larga',
                    'actual_chain': blockchain.to_json()}
    return jsonify(response), 200
##------------------------------------------------------------############################
app.run(host='192.168.0.104', port=5000)

