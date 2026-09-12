from flask import Flask, request
import os, requests

app = Flask(__name__)
TOKEN = os.environ.get("BOT_TOKEN")

def get_live_price(symbol):
    try:
        # Yahoo Finance se live price
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=5).json()
        price = r['chart']['result'][0]['meta']['regularMarketPrice']
        change = r['chart']['result'][0]['meta']['regularMarketPrice'] - r['chart']['result'][0]['meta']['previousClose']
        return price, change
    except:
        return None, None

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
            reply(chat_id, "Jai Shree Ram Bhai! 🙏\n\n<b>Nifty 76 Bot Ready Hai!</b>\n/nifty - Nifty 50 LIVE\n/banknifty - Bank Nifty LIVE\n/signals - Aaj ke Signals")

        elif msg == "/nifty":
            price, chg = get_live_price("^NSEI")
            if price:
                emoji = "🟢" if chg>=0 else "🔴"
                reply(chat_id, f"{emoji} <b>Nifty 50 LIVE</b>\n\nPrice: <b>{price:.2f}</b>\nChange: {chg:+.2f}\n\nTrend: {'Bullish' if chg>=0 else 'Bearish'} Hai Bhai!")
            else:
                reply(chat_id, "Market band hai Bhai, abhi price nahi aa raha!")

        elif msg == "/banknifty":
            price, chg = get_live_price("^NSEBANK")
            if price:
                emoji = "🟢" if chg>=0 else "🔴"
                reply(chat_id, f"{emoji} <b>Bank Nifty LIVE</b>\n\nPrice: <b>{price:.2f}</b>\nChange: {chg:+.2f}")
            else:
                reply(chat_id, "Bank Nifty data abhi nahi aa raha!")

        elif msg == "/signals":
            reply(chat_id, "🎯 <b>Aaj ka Signal (76 Strategy)</b>\n\nNIFTY 22500 CE BUY ABOVE 120\nSL: 80 | TGT: 150 / 200\n\nRisk apna dekh ke trade karna Bhai!")

        else:
            reply(chat_id, f"Tune bheja: {msg}\n/start dabaa!")
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
