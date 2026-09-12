from flask import Flask, request
import os
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>🚀 NIFTY 76 BOT LIVE - Webhook</h1>"

@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "ok", 200

@bot.message_handler(commands=['start'])
def start_cmd(m):
    bot.reply_to(m, "🔥 Bot LIVE hai! /nifty76 likho signal ke liye!")

@bot.message_handler(commands=['nifty76'])
def nifty_cmd(m):
    bot.reply_to(m, "📊 NIFTY 76 Signal - BUY Abhi (Test Message)")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
