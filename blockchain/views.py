from django.shortcuts import render
import datetime
import hashlib
import json
from uuid import uuid4
import requests
import sys
import socket
from urllib.parse import urlparse
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt #New

BLOCKCHAIN_REWARD_FACTOR = 210000


class Blockchain:
    def __init__(self, proof_of_work_diff=3):
        self.chain = []
        self.transactions = [] #New
        self.create_block(nonce = 1, previous_hash = '0')
        self.nodes = set() #New

        # my code 
        self.block_chain = [self.create_first_block()]
        self.proof_of_work_diff = proof_of_work_diff
        self.pending_transactions = []
        self.reward = BLOCKCHAIN_REWARD_FACTOR / len(self.block_chain)

    def create_first_block(self):
        first_transaction = Transaction("" , "", 0, 0)
        first_block = Block("", [first_transaction], datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))      
        return first_block
    
    def get_blockchain(self):
        return block_chain


    def get_pending_transactions(self):
        return len(self.pending_transactions)

    def create_block(self, nonce, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'nonce': nonce,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions #New
                }
        self.transactions = [] #New
        self.chain.append(block)
        return block

    
    def get_prev_hash(self):
        return self.block_chain[-1].hash


    def get_last_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_nonce):
        new_nonce = 1
        check_nonce = False
        while check_nonce is False:
            hash_operation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_nonce = True
            else:
                new_nonce += 1
        return new_nonce

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_nonce = previous_block['nonce']
            nonce = block['nonce']
            hash_operation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True


    def validate_blockchain(self):
        size_of_chain = len(self.block_chain)
        if( size_of_chain == 1 ):
            return JsonResponse({'message': f'BlockChain is valid!'})
        chain_index = 1
        
        while(chain_index >= size_of_chain):
            if(self.block_chain[chain_index].prev_hash != self.block_chain[chain_index - 1].hash):
                return JsonResponse({'message': f'BlockChain isnt valid!'})
        return JsonResponse({'message': f'BlockChain is valid!'})


    def add_transaction(self, sender, receiver, amount, time): #New
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount,
                                  'time': str(datetime.datetime.now())})
        previous_block = self.get_last_block()
        return previous_block['index'] + 1

    def get_last_block2(self):
        return self.blockchain[ len(self.blockchain) - 1 ]

   # def json_transactions(self, transactions):
    #    {}

    def mine(self, miner_name):
        print(self.pending_transactions)
        if(len(self.pending_transactions) == 0 ):
            return JsonResponse({'message': f'Block needs at least one transaction to mine'})

        # miner gets a transaction in reward for mining the block
        transaction_for_miner = Transaction("Iqbal_Coin", miner_name, self.reward, datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        prev_hash = self.get_prev_hash()
        block_to_mine = Block(prev_hash, self.pending_transactions, datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        
        if(block_to_mine.mine_block(self.proof_of_work_diff)):
            self.block_chain.append(block_to_mine)
            self.reward =  BLOCKCHAIN_REWARD_FACTOR / len(self.block_chain)
            self.pending_transactions = []
            return JsonResponse({'Mined block hash': block_to_mine.hash, 'Previous block hash': block_to_mine.prev_hash, 
                                'Transactions': (block_to_mine.get_transactions_json()), 'Date Created': block_to_mine.timestamp })
                                
        else:
            return 'Miner did not have enough computional resources to mine', HttpResponse(status=408)


    def add_transaction2(self, transaction):
        self.pending_transactions.append(transaction)
        
    
    def get_block(self, message):
        if 'id' != message[0]:
            return 'Needs specific id of block', HttpResponse(status_code=400)
        id = int(message['id'])
        if id > block_chain.length or id <= 0:
            return 'Id higher than amount of blocks in list or id is too low, (index starts at 1)', HttpResponse(status_code=401)

        block = block_chain[id - 1]
        return JsonResponse({'Mined block hash': block.hash, 'Previous block hash': block.prev_hash, 
                                'Transactions': str(block.transactions), 'Date Created': block.timestamp }) 

    def add_node(self, address): #New
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)


    def replace_chain(self): #New
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False



class Transaction :
    def __init__(self, sender, recipient, amount, datetime):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.datetime = datetime
        
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return str({"From Person": self.sender , "To Person": self.recipient, "Amount" : self.amount , "Date Created": self.datetime })
    
    def get_fields(self):
        return {'sender': self.sender, "recipient": self.recipient, "amount": self.amount, "datetime": self.datetime }



class Block:
    def __init__(self, prev_hash="", transactions=[], timestamp=""):
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.nonce = 0
        self.hash = self.make_hash()

    def __str__(self):
        return str({"previous hash": self.prev_hash , "Hash" : self.hash, "Transactions": str(self.transactions), "Timestamp" : self.timestamp})
    
    def __repr__(self):
        return str(self)

    def get_transactions_json(self):
        transaction_li = []
        for transaction in self.transactions:
            transaction_li.append(transaction.get_fields())
        return transaction_li
        

    def make_hash(self):
        rawData = str(self.prev_hash) + str(self.timestamp) + str(self.transactions) + str(self.nonce)
        encoded = json.dumps(rawData, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()

    def mine_block(self, proof_of_work_diff):
        hash_valid_temp = "0" * proof_of_work_diff
        while( self.hash[:proof_of_work_diff] != hash_valid_temp ):
            self.nonce += 1
            if(self.nonce == sys.maxsize):
                return False
            self.hash = self.make_hash()
        return True



# Creating our Blockchain
blockchain = Blockchain()
# Creating an address for the node running our server
node_address = str(uuid4()).replace('-', '') #New
root_node = 'e36f0158f0aed45b3bc755dc52ed4560d' #New


########################################Iqbals work###############

def mine_block2(request):
    if request.method == 'GET':
        return blockchain.mine('Jeff Bezos')

# this one needs work
@csrf_exempt
def get_block(request): 
    if request.method == 'GET':
        return blockchain.get_block( json.loads(request.body) )
        

@csrf_exempt
def validate_blockchain(request):
    if request.method == 'GET':
        return blockchain.validate_blockchain()



@csrf_exempt
def add_transaction2(request):
    if request.method == 'POST':
        received_json = json.loads(request.body)
        transaction_keys = ['sender', 'receiver', 'amount']
        
        if not all(key in received_json for key in transaction_keys):
            return 'Element(s) of transaction are missing', HttpResponse(status=400)

        new_transaction = Transaction(received_json['sender'], received_json['receiver'], received_json['amount'], str(datetime.datetime.now()))
        blockchain.add_transaction2( new_transaction )

        response = {'message': f'This transaction will is currently pending and will be added to the next Block once minded'}
        return JsonResponse(response)

def get_chain2(request):
    if request.method == 'GET':
        print("blockchain : ",  blockchain.get_blockchain()  )
        response = {'chain': blockchain.get_blockchain() , 
                    'length': len(blockchain.get_blockchain())
                }
        return JsonResponse(response)




########################################Iqbals work###############

# Getting the full Blockchain
def get_chain(request):
    if request.method == 'GET':
        response = {'chain': blockchain.chain,
                    'length': len(blockchain.chain)}
    return JsonResponse(response)



# Mining a new block
def mine_block(request):
    if request.method == 'GET':
        previous_block = blockchain.get_last_block()
        previous_nonce = previous_block['nonce']
        nonce = blockchain.proof_of_work(previous_nonce)
        previous_hash = blockchain.hash(previous_block)
        blockchain.add_transaction(sender = root_node, receiver = node_address, amount = 1.15, time=str(datetime.datetime.now()))
        block = blockchain.create_block(nonce, previous_hash)
        response = {'message': 'Congratulations, you just mined a block!',
                    'index': block['index'],
                    'timestamp': block['timestamp'],
                    'nonce': block['nonce'],
                    'previous_hash': block['previous_hash'],
                    'transactions': block['transactions']}
    return JsonResponse(response)





# Checking if the Blockchain is valid
def is_valid(request):
    if request.method == 'GET':
        is_valid = blockchain.is_chain_valid(blockchain.chain)
        if is_valid:
            response = {'message': 'All good. The Blockchain is valid.'}
        else:
            response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return JsonResponse(response)







# Adding a new transaction to the Blockchain
@csrf_exempt
def add_transaction(request): #New
    if request.method == 'POST':
        received_json = json.loads(request.body)
        transaction_keys = ['sender', 'receiver', 'amount','time']
        if not all(key in received_json for key in transaction_keys):
            return 'Some elements of the transaction are missing', HttpResponse(status=400)
        index = blockchain.add_transaction(received_json['sender'], received_json['receiver'], received_json['amount'],received_json['time'])
        response = {'message': f'This transaction will be added to Block {index}'}
    return JsonResponse(response)

# Connecting new nodes
@csrf_exempt
def connect_node(request): #New
    if request.method == 'POST':
        received_json = json.loads(request.body)
        nodes = received_json.get('nodes')
        if nodes is None:
            return "No node", HttpResponse(status=400)
        for node in nodes:
            blockchain.add_node(node)
        response = {'message': 'All the nodes are now connected. The Sudocoin Blockchain now contains the following nodes:',
                    'total_nodes': list(blockchain.nodes)}
    return JsonResponse(response)

# Replacing the chain by the longest chain if needed
def replace_chain(request): #New
    if request.method == 'GET':
        is_chain_replaced = blockchain.replace_chain()
        if is_chain_replaced:
            response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                        'new_chain': blockchain.chain}
        else:
            response = {'message': 'All good. The chain is the largest one.',
                        'actual_chain': blockchain.chain}
    return JsonResponse(response)