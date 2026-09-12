from flask import Flask, request
import requests, os

app = Flask(__name__)
BOT_TOKEN = os.environ.get("BOT_TOKEN")

def send_msg(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text","").lower()
        
        if "/start" in text:
            msg = """*Jai Shree Ram Bhai! 🚀*

*Nifty 76 Bot Ready Hai!*

Commands:
📊 `/nifty` - Nifty 50 Live
📈 `/banknifty` - Bank Nifty
🔥 `/signals` - Aaj ke signals

Bolo kya chahiye?"""
            send_msg(chat_id, msg)
        
        elif "nifty" in text or "bank" in text or "signal" in text:
            send_msg(chat_id, "Bhai abhi Nifty 76 ka full logic add kar raha hu... 2 min me live indicators aayenge! 📈")
        
    return "ok"

@app.route('/')
def home(): return "Nifty76 Bot Live - Jai Shree Ram"

if __name__ == "__main__":
    app.run()
