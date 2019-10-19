from time import time
import json
import hashlib
from uuid import uuid4
from urllib.parse import urlparse

class Blockchain :
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.neighbors = set()
        
        self.node_identifier = str(uuid4()).replace('-', '')
        
        self.diff = 4
        self.val_steps = 3
        
        self.new_block(prev_hash='0', proof=0)    
        
    def new_block(self, proof, prev_hash=None):
        '''
            This function creates a new block and appends it to the chain.
            
            parameters :
                proof = the Proof of Work
                prev_hash = the hash of the previous block in the chain
            
            returns :
                the new block
        '''
        if not prev_hash : prev_hash = self.hash(self.chain[-1])
        
        miner_transaction = self.new_transaction() 
        
        block = {
            'index' : len(self.chain) + 1,
            'prev_hash' : prev_hash,
            'time' : time(),
            'transactions' : self.current_transactions
        }
        
        proof = self.proof_of_work(block)
        block['proof'] = proof
        
        self.current_transactions = []
        self.chain.append(block)
        
        return block
    
    
    def new_transaction(self, sender, receiver, amount):
        '''
            This function creates a new transaction and appends it to the current_transactions.
            parameters : 
                sender = sender of the coin
                receiver = receiver of the coin
                amount = amount being sent
            
            returns : index of the block that will hold this transcation
        '''
        transaction = {'sender' : sender, 
                        'receiver' : receiver, 
                        'amount' : amount}
        
        self.current_transactions.append(transaction)
        self.broadcast_transaction(transaction)
        
        return self.chain[-1]['index'] + 1 
    
 	def new_neighbor(self, node):
        '''
            Add a new neighbor node to the node list.
            parameters : 
                neighbor = neighbor blockchain object
            returns :
                None
        '''
        self.nodes.add(node)
        return 
    
    def broadcast_transaction(self, transaction):
        for node in self.neighbors :
            node.current_transactions.append(transaction)
        
        return
               
    def hash(self, block):
        '''
            This function returns the SHA256 hash of the block.
        '''
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
        
    def valid_proof(self, block) :
        '''
            This function checks if the Proof of Work for a block is valid.
            parameters : 
                block = block for which to check the proof
            returns : 
                True if proof is valid, False otherwise
        '''
        proof = block['proof']
        temp_block = {i:block[i] for i in block if i != 'proof'}
        block_string = json.dumps(temp_block, sort_keys=True)
        
        guess = hashlib.sha256(f'{block_string}{proof}'.encode()).hexdigest()
        
        return guess[:self.diff] == '0'*self.diff
    

    def valid_chain(self, chain) :
        '''
            This function checks whether a given blockchain is valid.
            parameters :
                chain = the chain to be validated.
            returns : 
                True if chain is valid, False otherwise
        '''
        steps = self.val_steps
        prev_and_cur_block_indices = ((i-1, i) for i in range(len(chain)-steps-1, len(chain)-1,-1) if i-1 >= 0)
        
        for prev_ind, cur_ind in prev_and_cur_block_indices :
            if self.valid_proof(chain[cur_ind]) and \
               chain[cur_ind]['prev_hash'] == self.hash(chain[perv_ind]) : continue
            else :
                return False
        
        return True
    
    
    def proof_of_work(self, block):
        '''
            This function calculates the Proof of Work (PoW) for a given block.
            parameters : 
                block = the block for which PoW should be calculated
            
            returns :
                the proof (or nonce is literature)
        '''
        diff = self.diff
        block_string = json.dumps(block, sort_keys=True)
        
        proof = 0
        while True :
            guess = hashlib.sha256(f'{block_string}{proof}'.encode()).hexdigest()
            if guess[:diff] == '0'*diff : return proof
            else : proof += 1
    
        return -1
    
    def reach_consensus(self):
        '''
            This function implements a simple consensus algorithm that chooses the longest valid chain.
            parameters :
                None
            returns : 
                None, if there is no change in chain.
                new chain, otherwise
        '''
        chain_len = len(self.chain)
        new_chain = None
        
        for node in self.neighbors :
            chain = node.chain
            
            if len(chain) <= chain_len or not valid_chain(chain) : 
                continue
            else :
                new_chain = chain
        
        if new_chain : self.chain = new_chain
        
        return new_chain

            
