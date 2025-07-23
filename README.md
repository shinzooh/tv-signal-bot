# Shinzooh Trade API

Trading analysis API using Flask + xAI (Grok-4) + JSON input/output.

## Endpoint

- `GET /`: تأكيد التشغيل.

- `POST /analyze-with-xai`: تحليل مباشر باستخدام xAI.

## Environment Variables

- `XAI_API_KEY=your-xai-api-key-here`

## Usage

```bash
curl -X POST https://your-render-url/analyze-with-xai \
-H "Content-Type: application/json" \
-d '{"symbol": "XAUUSD", "frame": "15m", "data": "ما توقعك لحركة السعر القادمة؟"}'
