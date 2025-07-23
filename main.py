
from flask import Flask, request, jsonify
import requests
import os
import json

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ TV Signal Bot API is running."

@app.route('/analyze-with-xai', methods=['POST'])
def analyze_with_xai():
    data = request.json
    print("🔍 Request:", data)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('XAI_API_KEY')}"
    }

    payload = {
        "model": "grok-4-0709",
        "messages": [
            {"role": "user", "content": "Analyze this trading data: " + json.dumps(data)}
        ],
        "stream": False,
        "temperature": 0.7
    }

    response = requests.post("https://api.x.ai/v1/chat/completions", json=payload, headers=headers)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
