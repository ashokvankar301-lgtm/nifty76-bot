from flask import Flask, request
import os, requests

app = Flask(__name__)
TOKEN = os.environ.get("BOT_TOKEN")

def reply(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"})

@app.route("/")
def home():
    return "Nifty76 Bot Live Hai!"

@app.route("/webhook", methods=["POST"])
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        msg = data["message"].get("text", "")

        if msg == "/start":
            reply(chat_id, "Jai Shree Ram Bhai! 🙏\n\n<b>Nifty 76 Bot Ready Hai!</b>\n/nifty - Nifty 50 Live\n/banknifty - Bank Nifty Live\n/signals - Aaj ke Signals")
        elif msg == "/nifty":
            reply(chat_id, "📈 Nifty 50: 22,450 (Demo) \nTrend: Bullish Hai Bhai!")
        elif msg == "/banknifty":
            reply(chat_id, "🏦 Bank Nifty: 48,200 (Demo)\nTrend: Sideways")
        elif msg == "/signals":
            reply(chat_id, "🎯 Aaj ka Signal:\nNIFTY 22500 CE - BUY\nSL: 80 | Target: 150")
        else:
            reply(chat_id, f"Tune bheja: {msg}\n/start dabaa menu ke liye!")
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
