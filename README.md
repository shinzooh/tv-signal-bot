
# tv-signal-bot

A Flask-based API that receives trading signals and sends them for analysis using the xAI Grok-4-0709 model.

## Endpoints

- `/`: Health check.
- `/analyze-with-xai`: POST endpoint to analyze trading data via xAI API.

## Setup

1. Add your XAI API key in `.env` or environment variables.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   python main.py
   ```
