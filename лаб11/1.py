import hashlib
import time

# Функція для обчислення хешу блоку
def hash_block(data, prev_hash, nonce):
    block_string = str(data) + str(prev_hash) + str(nonce)
    return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

# Функція майнінгу 
def mine_block(block, difficulty=5):
    nonce = 0
    while True:
        block_hash = hash_block(block['data'], block['prev_hash'], nonce)
        if block_hash.startswith('0' * difficulty):
            block['nonce'] = nonce
            block['hash'] = block_hash
            return block
        nonce += 1

# Клас блоку
class Block:
    def __init__(self, data, prev_hash=''):
        self.data = data
        self.prev_hash = prev_hash
        self.nonce = None
        self.hash = None

    def mine(self, difficulty):
        mined_block = mine_block(self.__dict__, difficulty)
        self.nonce = mined_block['nonce']
        self.hash = mined_block['hash']

# Додаємо новий блок до ланцюга
def add_block(blockchain, data, difficulty=5):
    prev_hash = blockchain[-1].hash if blockchain else ''
    block = Block(data, prev_hash)
    block.mine(difficulty)
    blockchain.append(block)

# Створення всього блокчейну
def create_blockchain(values, difficulty=5):
    blockchain = []
    for value in values:
        add_block(blockchain, value, difficulty)
    return blockchain

# Вивід блоків
def print_blockchain(blockchain):
    for i, block in enumerate(blockchain):
        print(f"Block {i}")
        print(f"  Data      : {block.data}")
        print(f"  Prev Hash : {block.prev_hash}")
        print(f"  Nonce     : {block.nonce}")
        print(f"  Hash      : {block.hash}")
        print("-" * 60)

# Значення для запису
values = [91911, 90954, 95590, 97390, 96578, 97211, 95090]
difficulty = 5  

# Створюємо блокчейн
start = time.time()
blockchain = create_blockchain(values, difficulty)
end = time.time()

# Вивід результату
print_blockchain(blockchain)
print(f"\nBlockchain created in {round(end - start, 2)} seconds.")
