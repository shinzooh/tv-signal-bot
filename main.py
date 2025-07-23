from fastapi import FastAPI, HTTPException, Body
import requests
import os

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Shinzooh API ✅ جاهز"}  # حولتها JSON كاقتراح للاحترافية

@app.post("/analyze-with-xai")
async def analyze_with_xai(body: dict = Body(...)):
    symbol = body.get("symbol")
    frame = body.get("frame")
    data = body.get("data")
    
    if not all([symbol, frame, data]):
        raise HTTPException(status_code=400, detail="البيانات الناقصة: يجب توفير symbol, frame, data")
    
    # بناء الـ prompt بناءً على البيانات (يمكن تخصيصه أكثر)
    prompt = f"قم بتحليل حركة السعر لـ {symbol} في الإطار الزمني {frame}: {data}. أعطِ توقعاتك وأسبابك بالعربي."
    
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="مفتاح xAI API غير مضبوط في البيئة")
    
    url = "https://api.x.ai/v1/chat/completions"  # الـ endpoint الرسمي لـ xAI Grok API
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "grok-beta",  # أو "grok-4" إذا كان متاحًا (غيّره حسب اشتراكك)
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,  # لتحكم في الإبداع (يمكن تعديله)
        "max_tokens": 500  # حد أقصى للرد (لتجنب تكاليف عالية)
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # يرمي خطأ إذا فشل الطلب
        result = response.json()
        analysis = result["choices"][0]["message"]["content"]
        return {"analysis": analysis.strip()}  # إرجاع التحليل نظيفًا
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"خطأ في الاتصال بـ xAI API: {str(e)}")
    except KeyError:
        raise HTTPException(status_code=500, detail="هيكل الرد من xAI غير متوقع")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ غير متوقع: {str(e)}")
