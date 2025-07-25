from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
import requests
from urllib.parse import quote
import os

app = FastAPI(
    title="TV Signal Bot",
    description="بوت لجلب إشارات التداول من TradingView أو مصادر مشابهة، مع دعم تحليل xAI.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "message": "مرحباً في TV Signal Bot! السيرفر يعمل على FastAPI.",
        "routes": ["/signal", "/analyze-with-xai", "/health"]
    }

@app.get("/signal")
def get_signal(symbol: str = "BTCUSD"):
    try:
        api_url = f"https://api.coingecko.com/api/v3/simple/price?ids={quote(symbol.lower())}&vs_currencies=usd"
        response = requests.get(api_url)
        response.raise_for_status()

        data = response.json()
        if symbol.lower() in data:
            price = data[symbol.lower()]['usd']
            signal = "قوي" if price > 50000 else "ضعيف"
            return {
                "symbol": symbol,
                "price": price,
                "signal": signal,
                "message": "الإشارة مستخرجة بنجاح!"
            }
        else:
            return JSONResponse(status_code=404, content={"error": "الرمز غير موجود."})

    except requests.RequestException as e:
        return JSONResponse(status_code=500, content={"error": f"خطأ في جلب البيانات: {str(e)}"})

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/analyze-with-xai")
def analyze_with_xai(content: dict = Body(...)):
    try:
        symbol = content.get("symbol")
        frame = content.get("frame")
        data = content.get("data")

        if not all([symbol, frame, data]):
            return JSONResponse(status_code=400, content={"error": "البيانات ناقصة: symbol, frame, data"})

        api_key = os.getenv('XAI_API_KEY')
        if not api_key:
            return JSONResponse(status_code=500, content={"error": "XAI_API_KEY not set"})

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "messages": [
                {"role": "system", "content": "أنت مساعد مالي محترف. استخدم SMC وICT وRSI وMACD وEMA."},
                {"role": "user", "content": f"{symbol} - {frame}: {data}"}
            ],
            "model": "grok-4-0709",
            "stream": False,
            "temperature": 0
        }

        response = requests.post("https://api.x.ai/v1/chat/completions", headers=headers, json=payload)
        if response.status_code != 200:
            return JSONResponse(status_code=response.status_code, content={"error": response.text})

        result = response.json()
        analysis = result["choices"][0]["message"]["content"]

        return {
            "symbol": symbol,
            "frame": frame,
            "xai_analysis": analysis
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
