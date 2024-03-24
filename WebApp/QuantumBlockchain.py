from qiskit import QuantumCircuit, transpile, assemble
from qiskit.quantum_info import Operator
import hashlib
import random
from qiskit_aer import AerSimulator, Aer
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit.quantum_info import Operator
import math
import numpy as np
import fractions

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
        flags = [self.factor_flags(*self.shors_algorithm(num)) for num in last_numbers]
        prime_count = 0
        for f in flags: 
            if f == "11":
                prime_count += 1
        return prime_count

    def valid_proof(self, transactions, last_numbers, prime_count):
        actual_prime_count = self.count_primes(last_numbers)
        print(actual_prime_count)
        return actual_prime_count == prime_count
    
    def classical_modular_exponentiation(self, a, power, N):
        """Performs classical modular exponentiation."""
        return pow(a, int(power), int(N))

    def quantum_order_finding(self, a, N):
        """Performs the quantum part of the order-finding algorithm."""
        # Use Qiskit to construct the circuit for quantum order finding
        # This is a simplified version and might not work for all cases
        n = math.ceil(math.log2(N))
        qc = QuantumCircuit(2 * n, n)
        for q in range(n):
            qc.h(q)
        qc.x(n)
        for q in range(n):
            qc.append(Operator([[1, 0], [0, np.exp(2 * np.pi * 1j / (2 ** (q + 1)))]], input_dims=(2,)),
                    [q + n])
        qc.measure(range(n), range(n))
        
        # Transpile the circuit for the AerSimulator
        simulator = AerSimulator()
        transpiled_circuit = transpile(qc, simulator)
        
        # Execute the transpiled circuit
        job = simulator.run(transpiled_circuit, shots=1)
        result = job.result()
        measurements = list(result.get_counts().keys())[0]
        phase = int(measurements, 2) / (2 ** n)
        
        # Use classical methods to find the order from the phase
        frac = fractions.Fraction(phase).limit_denominator(N)
        r = frac.denominator
        return r

    def shors_algorithm(self, N, max_attempts=100):
        """Performs Shor's algorithm to factorize N."""
        if N <= 2:
            return 1, 0  # Return (1, 0) for numbers less than or equal to 2
        
        attempt = 0
        while attempt < max_attempts:
            # Step 1: Choose a random number a < N
            a = np.random.randint(2, N)
            
            # Step 2: Compute the greatest common divisor of a and N
            gcd = math.gcd(a, N)
            if gcd > 1:
                # We found a non-trivial factor
                return gcd, N // gcd
            
            # Step 3: Use the quantum algorithm to find the order r of a modulo N
            r = self.quantum_order_finding(a, N)
            
            # Step 4: If r is odd or a^(r/2) is congruent to -1 mod N, go back to step 1
            if r % 2 != 0 or self.classical_modular_exponentiation(a, r // 2, N) == N - 1:
                attempt += 1
                continue
            
            # Step 5: Compute the factors of N
            factor1 = math.gcd(self.classical_modular_exponentiation(a, r // 2, N) + 1, N)
            factor2 = math.gcd(self.classical_modular_exponentiation(a, r // 2, N) - 1, N)
            
            # Check if the factors are non-trivial
            if factor1 != 1 and factor2 != 1:
                return factor1, factor2
            else:
                attempt += 1

        return 1, 0  # Return (1, 0) if the algorithm fails

    def factor_flags(self, factor1, factor2):
        """Returns a binary flag based on the primality of the factors."""
        flag = ""
        if self.is_prime(factor1):
            flag += "1"
        else:
            flag += "0"
        if self.is_prime(factor2):
            flag += "1"
        else:
            flag += "0"
        return flag

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
