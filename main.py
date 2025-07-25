from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests  # لجلب البيانات من مصدر خارجي، مثل API للإشارات
from werkzeug.urls import url_quote  # لو تحتاج تشفر روابط أو نصوص (من Flask legacy، لكن متوافق)

app = FastAPI(
    title="TV Signal Bot",
    description="بوت لجلب إشارات التداول من TradingView أو مصادر مشابهة.",
    version="1.0.0"
)

# Endpoint أساسي للترحيب والاختبار
@app.get("/")
def read_root():
    return {"message": "مرحباً في TV Signal Bot! السيرفر يعمل على FastAPI. جرب /signal لجلب إشارة."}

# Endpoint لجلب إشارة (افتراضي: جلب بيانات من API عام، غيّر الـ URL حسب احتياجك)
@app.get("/signal")
def get_signal(symbol: str = "BTCUSD"):  # يأخذ رمز افتراضي، ممكن تغييره عبر query param مثل ?symbol=ETHUSD
    try:
        # مثال: جلب بيانات من API عام (مثل CoinGecko للعملات، غيّرها لـ TradingView API لو عندك مفتاح)
        api_url = f"https://api.coingecko.com/api/v3/simple/price?ids={url_quote(symbol.lower())}&vs_currencies=usd"
        response = requests.get(api_url)
        response.raise_for_status()  # يرفع خطأ لو الطلب فشل
        
        data = response.json()
        if symbol.lower() in data:
            price = data[symbol.lower()]['usd']
            signal = "قوي" if price > 50000 else "ضعيف"  # منطق بسيط، غيّره حسب احتياجك (مثل تحليل حقيقي)
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

# Endpoint إضافي للصحة (health check)، مفيد للـ monitoring في Render
@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}

# إذا تحتاج endpoints أكثر، أضفها هنا، مثلاً:
# @app.post("/custom-signal")
# def custom_signal(data: dict):
#     # كود لمعالجة بيانات واردة
#     return {"result": "معالجة ناجحة"}

# للتشغيل المحلي (تستينغ): 
# في الـ terminal: uvicorn main:app --reload --host 0.0.0.0 --port 8000
# ثم افتح http://localhost:8000/docs للواجهة Swagger

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)  # للتشغيل في Render، لكن Render يستخدم الأمر الخارجي
