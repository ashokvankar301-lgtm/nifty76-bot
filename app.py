from flask import Flask
import os, threading
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>🚀 NIFTY 76 BOT LIVE - Web OK + Bot OK</h1>"

@app.route('/alert')
def alert():
    return "Telegram OK"

@bot.message_handler(commands=['start'])
def start_cmd(m):
    bot.reply_to(m, "🚀 NIFTY 76 BOT LIVE\n\nBUY SIGNAL - Target 25000\nBot is working 24x7!")

@bot.message_handler(func=lambda m: True)
def all_msg(m):
    bot.reply_to(m, f"Hi {m.from_user.first_name}, Bot is LIVE ✅\nSend /start")

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
