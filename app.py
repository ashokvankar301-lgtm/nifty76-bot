import os, requests, threading, time
from flask import Flask, request
import yfinance as yf

BOT_TOKEN = "8942374145:AAHKpOwaoqhVD5i-jToSZX2tGN-MhZUTDTY"
app = Flask(__name__)

alerts = {}

def get_nifty_data(symbol="^NSEI"):
    try:
        t = yf.Ticker(symbol)
        data = t.history(period="1d", interval="1m").tail(1)
        if data.empty: return None
        price = round(float(data['Close'].iloc[-1]), 2)
        open_price = float(data['Open'].iloc[0])
        change = round(price - open_price, 2)
        pct = round((change/open_price)*100, 2)
        return price, change, pct
    except: return None

def send_msg(chat_id, text):
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                  json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})

def check_alerts():
    while True:
        try:
            info = get_nifty_data("^NSEI")
            if info:
                price, _, _ = info
                for chat_id, levels in list(alerts.items()):
                    for lvl in levels[:]:
                        if abs(price - lvl) <= 5:
                            send_msg(chat_id, f"🔔 *ALERT!* Nifty *{price}* ne *{lvl}* cross kiya!")
                            alerts[chat_id].remove(lvl)
        except: pass
        time.sleep(30)

threading.Thread(target=check_alerts, daemon=True).start()

@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text","").strip()
        if text == "/start":
            send_msg(chat_id, "Jai Shree Ram Bhai! 🚀\n\n*Nifty 76 Ready!*\n📊 /nifty - Live\n🏦 /banknifty\n🔔 /alert 23300")
        elif text.startswith("/nifty"):
            info = get_nifty_data("^NSEI")
            msg = f"📊 *NIFTY: {info[0]}* ({info[1]}, {info[2]}%)" if info else "Market band hai, Last: 23398.1"
            send_msg(chat_id, msg)
        elif text.startswith("/banknifty"):
            info = get_nifty_data("^NSEBANK")
            msg = f"🏦 *BANKNIFTY: {info[0]}*" if info else "Data nahi mila"
            send_msg(chat_id, msg)
        elif text.startswith("/alert"):
            parts = text.split()
            if len(parts)>1 and parts[1].replace('.','',1).isdigit():
                lvl=float(parts[1]); alerts.setdefault(chat_id, []).append(lvl)
                send_msg(chat_id, f"✅ Alert set: *{lvl}*")
            else:
                l=alerts.get(chat_id,[]); send_msg(chat_id, f"Alerts: {l}" if l else "Use: /alert 23300")
    return "ok",200

@app.route('/')
def home(): return "Nifty76 Live Running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
