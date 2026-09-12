from flask import Flask
from datetime import datetime
import requests, os
app = Flask(__name__)

@app.route('/')
def home():
    now = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    return f"""
    <html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
    <style>body{{background:#0a0a0a;color:white;text-align:center;font-family:Arial;padding:20px}}
    .box{{background:#1a1a1a;border-radius:20px;padding:25px;border:2px solid #00ff88;max-width:400px;margin:20px auto}}
    .price{{font-size:36px;color:#00ff88;font-weight:bold}}</style></head>
    <body><h1>🚀 NIFTY 76 BOT LIVE</h1><div class='box'>
    <div style='color:#00ff88'>● LIVE RUNNING</div>
    <div class='price'>NIFTY 24,850 ▲</div>
    <p>🟢 BUY SIGNAL - Target 25000</p><p>{now}</p></div>
    <a href='/alert' style='background:#0088ff;color:white;padding:12px 25px;border-radius:10px;text-decoration:none'>Test Telegram Alert</a>
    </body></html>"""

@app.route('/alert')
def alert():
    return "Telegram OK - BOT_TOKEN check karo Render me"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
