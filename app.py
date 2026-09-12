import os
from flask import Flask, request
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8942374145:AAHKpOwaoqhVD5i-jToSZX2tGN-MhZUTDTY")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Jai Shree Ram Bhai! Bot Live ho gaya hai 🚀 Nifty 76 ready hai!")

@bot.message_handler(func=lambda m: True)
def all_msg(message):
    bot.reply_to(message, "Bolo kya chahiye?")

@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "ok", 200

@app.route('/')
def home():
    return "Nifty76 Bot is Live!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
