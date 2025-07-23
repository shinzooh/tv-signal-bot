from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Shinzooh API ✅ جاهز", "status": "ok"})

@app.route('/analyze-with-xai', methods=['POST'])
def analyze_with_xai():
    try:
        content = request.get_json()
        symbol = content.get('symbol')
        frame = content.get('frame')
        prompt = content.get('data')

        if not all([symbol, frame, prompt]):
            return jsonify({'error': 'البيانات ناقصة: symbol, frame, data'}), 400

        api_key = os.getenv('XAI_API_KEY')
        if not api_key:
            return jsonify({'error': 'XAI_API_KEY not set'}), 500

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "messages": [
                {"role": "system", "content": "أنت مساعد مالي محترف. استخدم SMC وICT وRSI وMACD وEMA."},
                {"role": "user", "content": f"{symbol} - {frame}: {prompt}"}
            ],
            "model": "grok-4-0709",
            "stream": False,
            "temperature": 0.7
        }

        response = requests.post("https://api.x.ai/v1/chat/completions", headers=headers, json=payload)
        if response.status_code != 200:
            return jsonify({'error': response.text}), response.status_code

        result = response.json()
        analysis = result["choices"][0]["message"]["content"]

        return jsonify({
            'symbol': symbol,
            'frame': frame,
            'input': prompt,
            'result': analysis
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
