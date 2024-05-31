import hashlib
import time


class BlockchainBlock:
    def __init__(self, index, previous_hash, timestamp, data, block_hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.block_hash = block_hash


class Blockchain:
    def __init__(self):
        self.blockchain = [self.create_genesis_block()]
        self.last_block = self.blockchain[0]

    @staticmethod
    def calculate_hash(index, previous_hash, timestamp, data):
        value = str(index) + str(previous_hash) + str(timestamp) + str(data)
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    def create_genesis_block(self):
        return BlockchainBlock(
            0,
            "0",
            int(time.time()),
            "Genesis Block",
            self.calculate_hash(0, "0", int(time.time()), "Genesis Block"),
        )

    def create_new_block(self, data):
        index = self.last_block.index + 1
        timestamp = int(time.time())
        block_hash = self.calculate_hash(
            index, self.last_block.block_hash, timestamp, str(data)
        )
        return BlockchainBlock(
            index, self.last_block.block_hash, timestamp, data, block_hash
        )

    def add_block(self, data):
        new_block = self.create_new_block(data)
        self.blockchain.append(new_block)
        self.last_block = new_block
        return new_block


blockchain = Blockchain()
