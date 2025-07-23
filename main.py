from flask import Flask, request, jsonify
from werkzeug.urls import url_quote

app = Flask(__name__)

@app.route('/')
def home():
    return "Shinzooh API ✅ جاهز"

@app.route('/analyze-with-xai', methods=['POST'])
def analyze_with_xai():
    try:
        req = request.get_json()
        symbol = req.get("symbol", "")
        frame = req.get("frame", "")
        data = req.get("data", "")

        result = {
            "symbol": symbol,
            "frame": frame,
            "xai_analysis": f"تحليل الذكاء الصناعي: {data} ✅"
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
