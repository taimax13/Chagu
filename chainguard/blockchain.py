import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        genesis_block = Block(0, "0", int(time.time()), "Genesis Block", "0")
        genesis_block.hash = self.calculate_hash(genesis_block)
        return genesis_block

    def calculate_hash(self, block):
        block_string = f"{block.index}{block.previous_hash}{block.timestamp}{block.data}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        latest_block = self.get_latest_block()
        new_block = Block(len(self.chain), latest_block.hash, int(time.time()), data, "")
        new_block.hash = self.calculate_hash(new_block)
        self.chain.append(new_block)
        print(f"Block added: {new_block.hash}")
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != self.calculate_hash(current_block):
                return False

            if current_block.previous_hash != previous_block.hash:
                return False
        return True
