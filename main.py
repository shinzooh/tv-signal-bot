import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def health_check():
    return jsonify({"status": "ok", "message": "tv-signal-bot is running."})

@app.route("/analyze-with-xai", methods=["POST"])
def analyze_with_xai():
    data = request.json
    print("🔍 Request Received:", data)

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

    try:
        response = requests.post("https://api.x.ai/v1/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as http_err:
        print("HTTP error occurred:", http_err)
        return jsonify({"error": str(http_err)}), response.status_code
    except Exception as err:
        print("Other error occurred:", err)
        return jsonify({"error": str(err)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
