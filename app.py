from flask import Flask
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def home():
    return f"<h1>🔥 NIFTY 76 BOT LIVE HAI BHAI 🔥</h1><p>{datetime.now()}</p><p>BUY SIGNAL</p>"

@app.route('/alert')
def alert():
    return "Alert OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
