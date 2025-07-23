from flask import Flask, jsonify, request
import json
import os
import requests

app = Flask(__name__)

# Load sample JSON data
try:
    with open('data/sample_all_data.json', 'r') as f:
        sample_data = json.load(f)
except FileNotFoundError:
    sample_data = {"error": "sample_all_data.json not found"}

# Load full JSON data
try:
    with open('all_data.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    data = {"error": "all_data.json not found"}

@app.route('/')
def home():
    return "Shinzooh API is live ✅"

@app.route('/data')
def get_data():
    return jsonify(data)

@app.route('/data/sample')
def get_sample_data():
    return jsonify(sample_data)

@app.route('/webhook', methods=['POST'])
def webhook():
    webhook_data = request.json
    print("🚨 Webhook Received:", webhook_data)
    with open('webhook_log.json', 'a') as f:
        f.write(json.dumps(webhook_data) + '\n')
    return jsonify({"status": "received"})

@app.route('/analyze-with-xai', methods=['POST'])
def analyze_with_xai():
    try:
        data = request.json
        api_key = os.getenv('XAI_API_KEY')
        if not api_key:
            return jsonify({"error": "XAI_API_KEY not set"}), 500

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "grok-4-0709",
            "messages": [
                {"role": "user", "content": f"Analyze this trading data for SMC/ICT + RSI/EMA/MACD: {json.dumps(data)}"}
            ],
            "stream": False,
            "temperature": 0.7
        }

        response = requests.post("https://api.x.ai/v1/chat/completions", json=payload, headers=headers)
        if response.status_code != 200:
            return jsonify({"error": response.text}), response.status_code

        xai_result = response.json()
        result = {
            "symbol": data.get("symbol"),
            "frame": data.get("frame"),
            "xai_analysis": xai_result.get("choices", [{}])[0].get("message", {}).get("content"),
            "confidence_score": 0.93,
            "recommendation": "Buy" if "bullish" in xai_result.get("choices", [{}])[0].get("message", {}).get("content", "").lower() else "Sell"
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)