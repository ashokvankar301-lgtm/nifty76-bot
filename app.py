from flask import Flask, request
import requests
import os

BOT_TOKEN = "8942374145:AAEhexwYywcxqok-GzZQxxcMxgyFD1mz_Mg"
CHAT_ID = "997066784"

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Nifty 76 Bot is Live! Bhai ka Bot Chal Raha Hai!"

@app.route('/alert', methods=['POST'])
def alert():
    try:
        data = request.get_json(force=True, silent=True) or {}
        msg = data.get('message', str(data))
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=10)
        return "OK", 200
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
