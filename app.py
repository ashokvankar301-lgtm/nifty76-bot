from flask import Flask, request
import os
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>🚀 NIFTY 76 BOT LIVE - Webhook Active</h1>"

@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "ok", 200
    else:
        return "error", 403

@bot.message_handler(commands=['start'])
def start_cmd(m):
    bot.reply_to(m, "🔥 Bot LIVE hai! /nifty76 bhejo signal ke liye")

@bot.message_handler(commands=['nifty76'])
def nifty_cmd(m):
    bot.reply_to(m, "📊 NIFTY 76 Signal - Working!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
