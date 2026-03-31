import hashlib
import json
from datetime import datetime

class Block:
    def __init__(self, index, previous_hash, data):
        self.index = index
        self.timestamp = str(datetime.now())
        self.previous_hash = previous_hash
        self.data = data
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_info = {
            "index": self.index,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "data": self.data,
            "nonce": self.nonce
        }
        block_string = json.dumps(block_info, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine(self, difficulty=3):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block #{self.index} mined! Hash: {self.hash}")

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", "Genesis Block - Start of Chain")

    def add_block(self, data):
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), last_block.hash, data)
        new_block.mine(difficulty=3)          # Easy difficulty for quick demo
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def show(self):
        print("\n" + "="*60)
        print("          SIMPLE BLOCKCHAIN")
        print("="*60)
        for block in self.chain:
            print(f"\nBlock #{block.index}")
            print(f"Time     : {block.timestamp}")
            print(f"Data     : {block.data}")
            print(f"Prev Hash: {block.previous_hash[:20]}...")
            print(f"Hash     : {block.hash}")
            print(f"Nonce    : {block.nonce}")
        print("="*60)

# ========================
# Run Demo
# ========================
if __name__ == "__main__":
    print("🚀 Starting Minimal Blockchain Demo...\n")
    
    bc = Blockchain()
    
    bc.add_block({"sender": "Alice", "receiver": "Bob", "amount": 50})
    bc.add_block({"sender": "Bob", "receiver": "Charlie", "amount": 25})
    bc.add_block({"sender": "Charlie", "receiver": "Alice", "amount": 10})
    
    bc.show()
    
    print("\n✅ Is the blockchain valid?", bc.is_valid())
    
    # Demonstrate tampering
    print("\n🔧 Tampering with Block 1 data...")
    bc.chain[1].data = {"sender": "Alice", "receiver": "Bob", "amount": 9999}
    print("✅ Is the blockchain still valid?", bc.is_valid())
