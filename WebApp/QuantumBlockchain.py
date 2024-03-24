from qiskit_aer import Aer
from qiskit import QuantumCircuit, transpile, assemble
import hashlib
import random

class QuantumBlockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(numbers=self.generate_random_numbers(), prime_count=0, previous_hash='0')  # Genesis block

    def create_block(self, numbers, prime_count, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'transactions': self.current_transactions,
            'numbers': numbers,
            'prime_count': prime_count,
            'previous_hash': previous_hash
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    def hash(self, block):
        block_string = str(block).encode()
        return hashlib.sha256(block_string).hexdigest()

    def generate_random_numbers(self):
        return [random.randint(1, 100) for _ in range(20)]

    def is_prime(self, n):
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def count_primes(self, numbers):
        return sum(1 for number in numbers if self.is_prime(number))

    def valid_proof(self, transactions, last_numbers, prime_count):
        actual_prime_count = self.count_primes(last_numbers)
        print(actual_prime_count)
        return actual_prime_count == prime_count

# Example usage
blockchain = QuantumBlockchain()
print(blockchain.chain)

# Add a new transaction
blockchain.add_transaction(sender="Alice", recipient="Bob", amount=100)

# Suppose a miner has found the prime count for the last block's numbers
last_block = blockchain.last_block
last_numbers = last_block['numbers']
prime_count = 6  # Placeholder for the actual prime count found by the miner

# If the proof is valid, create a new block
if blockchain.valid_proof(blockchain.current_transactions, last_numbers, prime_count):
    previous_hash = blockchain.hash(last_block)
    new_numbers = blockchain.generate_random_numbers()
    block = blockchain.create_block(new_numbers, prime_count, previous_hash)

print(blockchain.chain)
