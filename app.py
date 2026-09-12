from flask import Flask, request
import os, requests, datetime
app = Flask(__name__)
TOKEN = os.environ.get("BOT_TOKEN")
def send(chat_id, text, buttons=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if buttons:
        data["reply_markup"] = {"inline_keyboard": buttons}
    requests.post(url, json=data)
def live(symbol):
    try:
        r = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}", headers={"User-Agent":"Mozilla/5.0"}, timeout=5).json()
        meta = r['chart']['result'][0]['meta']
        return meta['regularMarketPrice'], meta['regularMarketPrice'] - meta['previousClose']
    except:
        return None, None

@app.route("/")
def home(): return "Nifty76 ALL GREAT LIVE!"
@app.route("/webhook", methods=["POST"])
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        msg = data["message"].get("text","").lower()
        if "/start" in msg:
            btns = [[{"text":"📈 Nifty Live","callback_data":"nifty"},{"text":"🏦 BankNifty","callback_data":"bank"}]]
            send(chat_id, "Jai Shree Ram Bhai! 🙏\n<b>🔥 Nifty 76 - ALL GREAT BOT 🔥</b>", btns)
        elif "/nifty" in msg:
            p,c = live("^NSEI")
            if p: send(chat_id, f"{'🟢' if c>=0 else '🔴'} <b>NIFTY {p:.2f} ({c:+.2f})</b>")
        elif "bank" in msg:
            p,c = live("^NSEBANK")
            if p: send(chat_id, f"🏦 <b>BANK NIFTY {p:.2f} ({c:+.2f})</b>")
        elif "signal" in msg:
            p,c = live("^NSEI")
            send(chat_id, f"🎯 <b>76 SIGNAL:</b> Nifty {p} pe trade dekho Bhai!")
        elif "chart" in msg:
            send(chat_id, "📊 Chart: https://in.tradingview.com/symbols/NSE-NIFTY/")
    if "callback_query" in data:
        q = data["callback_query"]
        chat_id = q["message"]["chat"]["id"]
        d = q["data"]
        p,c = live("^NSEI")
        if d=="nifty": send(chat_id, f"📈 Nifty: {p}")
        if d=="bank":
            p,c = live("^NSEBANK")
            send(chat_id, f"🏦 Bank: {p}")
    return "ok"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
