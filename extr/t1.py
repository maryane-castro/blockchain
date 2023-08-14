import hashlib
import time

class Block:
    def __init__(self, index, timestamp, document_data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.document_data = document_data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
        
    def calculate_hash(self):
        data = str(self.index) + str(self.timestamp) + str(self.document_data) + str(self.previous_hash) + str(self.nonce)
        return hashlib.sha256(data.encode('utf-8')).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        
    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")
        
    def get_latest_block(self):
        return self.chain[-1]
        
    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)
        
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
            
        return True


blockchain = Blockchain()


blockchain.add_block(Block(1, time.time(), "Documento 1", blockchain.get_latest_block().hash))
blockchain.add_block(Block(2, time.time(), "Documento 2", blockchain.get_latest_block().hash))
blockchain.add_block(Block(5, time.time(), "Documento 3", blockchain.get_latest_block().hash))

# Verifique a integridade da cadeia
print("A cadeia é válida?", blockchain.is_chain_valid())

# Imprima a cadeia de blocos
for block in blockchain.chain:
    print(f"Índice: {block.index}")
    print(f"Timestamp: {block.timestamp}")
    print(f"Documento: {block.document_data}")
    print(f"Hash anterior: {block.previous_hash}")
    print(f"Hash atual: {block.hash}")
    print("-------------------------------")