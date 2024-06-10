from flask import Flask, jsonify, request
from flask_dotenv import DotEnv
from wallet import Wallet  

app = Flask(__name__)
env = DotEnv(app)
app.config.from_envvar('YOUR_ENV_FILE_PATH')

wallet = Wallet()

@app.route('/wallet/create', methods=['POST'])
def create_wallet():
    wallet_id, private_key = wallet.create_wallet()
    if wallet_id:
        return jsonify({"wallet_id": wallet_id, "private_key": private_key}), 200
    else:
        return jsonify({"error": "Unable to create wallet"}), 500

@app.route('/wallet/balance/<string:wallet_id>', methods=['GET'])
def get_wallet_balance(wallet_id):
    balance = wallet.get_balance(wallet_id)
    if balance is not None:
        return jsonify({"wallet_id": wallet_id, "balance": balance}), 200
    else:
        return jsonify({"error": "Wallet not found"}), 404

@app.route('/wallet/send', methods=['POST'])
def send_transaction():
    sender_wallet_id = request.json.get('sender_wallet_id')
    recipient_wallet_id = request.json.get('recipient_wallet_id')
    amount = request.json.get('amount')
    
    if not sender_wallet_id or not recipient_wallet_id or not amount:
        return jsonify({"error": "Missing data"}), 400

    transaction_hash = wallet.send_transaction(sender_wallet_id, recipient_wallet_id, amount)
    if transaction_hash:
        return jsonify({"transaction": transaction_hash}), 200
    else:
        return jsonify({"error": "Transaction failed"}), 500

if __name__ == '__main__':
    app.run(debug=True)