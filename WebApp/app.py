from flask import Flask, jsonify, render_template, request
# from QuantumBlockchain import QuantumBlockchain
from QuantumBlockchain import QuantumBlockchain

app = Flask(__name__)
blockchain = QuantumBlockchain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json(force=True)
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = blockchain.add_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block 
    last_prime_count = last_block['prime_count']
    prime_count = blockchain.count_primes(last_block['numbers'])  # Placeholder for actual mining process

    
    new_block_mined = blockchain.valid_proof(blockchain.current_transactions, last_block['numbers'], prime_count)
    if new_block_mined:
        previous_hash = blockchain.hash(last_block)
        new_numbers = blockchain.generate_random_numbers()
        block = blockchain.create_block(new_numbers, prime_count, previous_hash)
        print(block)
        response = {
            'message': 'New block mined',
            'index': block['index'],
            'transactions': block['transactions'],
            'numbers': block['numbers'],
            'prime_count': block['prime_count'],
            'previous_hash': block['previous_hash'],
        }
    else:
        response = {'message': 'No new block mined'}

    return jsonify(response), 200



if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=8000)
