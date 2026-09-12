import os
import yfinance as yf
from flask import Flask, request
import requests
import threading
import time

BOT_TOKEN = os.environ.get("BOT_TOKEN")
app = Flask(__name__)

alerts = {}

def get_live(symbol):
    try:
        d = yf.Ticker(symbol).history(period="1d")
        if d.empty: return None
        return round(float(d['Close'].iloc[-1]), 2)
    except:
        return None

def send_msg(chat_id, text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": text})
    except:
        pass

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"].strip()

        if text == "/start":
            send_msg(chat_id, "Nifty76 Live Bot Ready! 🚀\n/nifty - Live Nifty\n/banknifty - Live BankNifty\n/alert 24500 - Set Alert")
        elif text == "/nifty":
            p = get_live("^NSEI")
            if p:
                send_msg(chat_id, f"📈 NIFTY 50: {p}")
            else:
                send_msg(chat_id, "Market closed hai bhai")
        elif text == "/banknifty":
            p = get_live("^NSEBANK")
            if p:
                send_msg(chat_id, f"🏦 BANKNIFTY: {p}")
            else:
                send_msg(chat_id, "Market closed")
        elif text.startswith("/alert"):
            try:
                level = float(text.split()[1])
                alerts[chat_id] = level
                send_msg(chat_id, f"✅ Alert set at {level}")
            except:
                send_msg(chat_id, "Use: /alert 24500")
    return "ok"

@app.route('/')
def home():
    return "Nifty76 Bot Live"

if __name__ == "__main__":
    app.run()
