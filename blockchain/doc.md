## Blockchain Implementation in Python

This code provides a simple implementation of a blockchain using Python. The main components are the `BlockchainBlock` class and the `Blockchain` class.

### BlockchainBlock Class

The `BlockchainBlock` class represents an individual block in the blockchain. Each block contains:
- `index`: The position of the block in the blockchain.
- `previous_hash`: The hash of the previous block in the blockchain.
- `timestamp`: The time when the block was created.
- `data`: The data stored in the block.
- `block_hash`: The hash of the current block, which is calculated using the `calculate_hash` method.

### Blockchain Class

The `Blockchain` class manages the chain of blocks. It includes the following methods and properties:

#### Properties

- `blockchain`: A list that stores the blocks. It starts with the genesis block.
- `last_block`: A reference to the most recently added block in the blockchain.

#### Methods

- `__init__`: Initializes the blockchain with the genesis block and sets `last_block` to the genesis block.
- `calculate_hash`: A static method that takes the `index`, `previous_hash`, `timestamp`, and `data` of a block and returns a SHA-256 hash. This hash is used to ensure the integrity of the block.
- `create_genesis_block`: Creates the first block in the blockchain, known as the genesis block. The genesis block has a fixed index of 0 and a `previous_hash` of "0".
- `create_new_block`: Creates a new block with the given `data`. The new block's `index` is the `index` of the last block plus one. The `timestamp` is the current time, and the `block_hash` is calculated using the `calculate_hash` method.
- `add_block`: Adds a new block with the given `data` to the blockchain. It creates a new block using `create_new_block`, appends it to the `blockchain`, updates `last_block` to the new block, and returns the new block.

### Example Usage

The code includes an instance of the `Blockchain` class called `blockchain`, which can be used to add and manage blocks in the blockchain. Here's an example of how to use it:

```python
blockchain = Blockchain()
new_block = blockchain.add_block("Some transaction data")
print(new_block.index)
print(new_block.data)
print(new_block.block_hash)
