from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Initial state: bot is locked
bot_status = {
    "is_locked": True,
    "fuel_level": 0,
    "chain": None,
    "duration": None
}

# Define chain-specific deposit requirements (example values)
chain_deposit_requirements = {
    "solana": 10,  # e.g., 10 SOL
    "evm": 0.1,    # e.g., 0.1 ETH
    "tron": 100    # e.g., 100 TRX
}

@app.route('/')
def index():
    return render_template('index.html', bot_status=bot_status, chain_deposit_requirements=chain_deposit_requirements)

@app.route('/unlock-bot', methods=['POST'])
def unlock_bot():
    global bot_status
    
    chain = request.form.get('chain')
    deposit_amount = float(request.form.get('deposit_amount'))
    
    # Check if deposit meets the requirement for the selected chain
    if deposit_amount >= chain_deposit_requirements.get(chain, 0):
        # Unlock the bot and set the fuel level
        bot_status["is_locked"] = False
        bot_status["fuel_level"] = deposit_amount
        bot_status["chain"] = chain
        bot_status["duration"] = request.form.get('duration')
        return jsonify({"status": "success", "message": "Bot unlocked successfully!"})
    else:
        return jsonify({"status": "failure", "message": "Insufficient deposit amount!"})

@app.route('/status')
def status():
    return jsonify(bot_status)

if __name__ == '__main__':
    app.run(debug=True)
