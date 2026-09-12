from flask import Flask, request
import os, requests, yfinance as yf, pandas as pd
from datetime import datetime

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN","").strip()
API = f"https://api.telegram.org/bot{TOKEN}" if TOKEN else ""

def send(chat_id, text):
    if API:
            try:
                        requests.post(f"{API}/sendMessage", json={"chat_id":chat_id,"text":text,"parse_mode":"Markdown"}, timeout=10)
                                except: pass

                                def get_nifty_data():
                                    try:
                                            # Nifty data
                                                    ticker = yf.Ticker("^NSEI")
                                                            hist = ticker.history(period="2d")
                                                                    if len(hist)>=2:
                                                                                today = hist.iloc[-1].Close
                                                                                            yest = hist.iloc[-2].Close
                                                                                                        ch = today-yest
                                                                                                                    pct = (ch/yest)*100
                                                                                                                                return today, ch, pct
                                                                                                                                    except: pass
                                                                                                                                        return 18000, 0, 0

                                                                                                                                        @app.route('/')
                                                                                                                                        def home():
                                                                                                                                            return "Nifty76 Bot Running!"

                                                                                                                                            @app.route(f'/{TOKEN}', methods=['POST'])
                                                                                                                                            def webhook():
                                                                                                                                                data = request.get_json()
                                                                                                                                                    if not data or 'message' not in data:
                                                                                                                                                            return "ok",200
                                                                                                                                                                chat = data['message']['chat']['id']
                                                                                                                                                                    text = data['message'].get('text','').lower()

                                                                                                                                                                        if '/start' in text:
                                                                                                                                                                                send(chat, "🚀 *Nifty76 Bot Ready!*\n\n/nifty76 - Chart bhejo\n/start - ye message")
                                                                                                                                                                                    elif 'nifty76' in text or '/nifty' in text:
                                                                                                                                                                                            price, ch, pct = get_nifty_data()
                                                                                                                                                                                                    emo = "🟢" if ch>=0 else "🔴"
                                                                                                                                                                                                            msg = f"{emo} *NIFTY 50*\n\nPrice: {price:.2f}\nChange: {ch:+.2f} ({pct:+.2f}%)\n\n_Time: {datetime.now().strftime('%d-%m %H:%M')}_"
                                                                                                                                                                                                                    send(chat, msg)
                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                send(chat, f"Samjha nahi: {text}\n/nifty76 likho")
                                                                                                                                                                                                                                    return "ok",200

                                                                                                                                                                                                                                    if __name__ == "__main__":
                                                                                                                                                                                                                                        app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))