import os
from flask import Flask, request
import requests

app = Flask(__name__)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route('/')
def home():
    return "Bot is running!"

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        if text == "/start":
            msg = "🔥 Nifty76 Bot Live hai! Welcome!"
        else:
            msg = f"Tune bheja: {text}"
            
        requests.post(f"{TELEGRAM_API}/sendMessage", json={"chat_id": chat_id, "text": msg})
    
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
