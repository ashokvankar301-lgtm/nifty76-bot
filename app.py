import os
import requests
from flask import Flask, request

BOT_TOKEN = "8942374145:AAHKpOwaoqhVD5i-jToSZX2tGN-MhZUTDTY"
app = Flask(__name__)

@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        if text == "/start":
            reply = "Jai Shree Ram Bhai! 🚀 Bot Live ho gaya hai! Nifty 76 ready hai!"
        else:
            reply = "Bolo kya chahiye?"
        
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      json={"chat_id": chat_id, "text": reply})
    return "ok", 200

@app.route('/')
def home():
    return "Nifty76 Bot is Live!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
