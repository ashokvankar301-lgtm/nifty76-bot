from flask import Flask, request
import os, requests, datetime

app = Flask(__name__)
TOKEN = os.environ.get("BOT_TOKEN")

def send(chat_id, text, buttons=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}
    if buttons:
        data["reply_markup"] = {"inline_keyboard": buttons}
    requests.post(url, json=data)

def live(sym):
    try:
        r = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}", headers={"User-Agent":"Mozilla/5.0"}, timeout=5).json()
        m = r['chart']['result'][0]['meta']
        price = m['regularMarketPrice']
        change = price - m['previousClose']
        pct = (change/m['previousClose'])*100
        return price, change, pct
    except:
        return None, None, None

def get_76_levels(price):
    atm = round(price/100)*100
    return {"CE": atm+100, "PE": atm-100, "SL": round(price*0.996,2), "TGT1": round(price*1.004,2), "TGT2": round(price*1.008,2)}

def main_menu():
    return [[{"text":"📈 Nifty","callback_data":"nifty"}, {"text":"🏦 Bank","callback_data":"bank"}],
            [{"text":"🎯 76 Signal","callback_data":"signal"}, {"text":"📊 Chart","callback_data":"chart"}],
            [{"text":"💹 Sensex","callback_data":"sensex"}, {"text":"🔥 Finnifty","callback_data":"finnifty"}]]

@app.route("/")
def home(): return "Nifty76 BEST BOT LIVE!"

@app.route("/webhook", methods=["POST"])
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data: return "ok"

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        msg = data["message"].get("text","").lower().strip()

        if "/start" in msg or "hi" in msg or "hello" in msg:
            send(chat_id, "Jai Shree Ram Bhai! 🙏\n\n🔥 <b>Nifty 76 - BEST BOT</b> 🔥\n\nSabse Best Features Ready Hai:\n✅ Live Price\n✅ 76 Strategy Signal\n✅ Chart & Levels\n\nNiche button dabao:", main_menu())

        elif "/nifty" in msg or msg=="nifty":
            p,c,pct = live("^NSEI")
            lvl = get_76_levels(p) if p else {}
            txt = f"{'🟢' if c>=0 else '🔴'} <b>NIFTY 50 LIVE</b>\n\nPrice: <b>{p:.2f}</b>\nChange: {c:+.2f} ({pct:+.2f}%)\n\n<b>76 Levels:</b>\nSupport: {lvl.get('SL')}\nTGT1: {lvl.get('TGT1')}\nTGT2: {lvl.get('TGT2')}\n\nTrend: {'Bullish 🚀' if c>=0 else 'Bearish 📉'}"
            send(chat_id, txt, main_menu())

        elif "bank" in msg:
            p,c,pct = live("^NSEBANK")
            send(chat_id, f"🏦 <b>BANK NIFTY</b>\n\nPrice: <b>{p:.2f}</b>\nChange: {c:+.2f} ({pct:+.2f}%)\nTrend: {'Bullish' if c>=0 else 'Bearish'}", main_menu())

        elif "sensex" in msg:
            p,c,pct = live("^BSESN")
            send(chat_id, f"💹 <b>SENSEX LIVE</b>\n\nPrice: <b>{p:.2f}</b>\nChange: {c:+.2f}", main_menu())

        elif "finnifty" in msg:
            p,c,pct = live("^CNXFIN")
            send(chat_id, f"🔥 <b>FINNIFTY LIVE</b>\n\nPrice: <b>{p:.2f}</b>\nChange: {c:+.2f}", main_menu())

        elif "signal" in msg:
            p,c,pct = live("^NSEI")
            lvl = get_76_levels(p)
            txt = f"🎯 <b>76 STRATEGY - {datetime.date.today()}</b>\n\nNifty: <b>{p:.2f}</b>\n\n<b>CE Trade:</b>\nBuy {lvl['CE']} CE Above {p*1.001:.0f}\nSL: {lvl['SL']}\nTGT: {lvl['TGT1']} / {lvl['TGT2']}\n\n<b>PE Trade:</b>\nBuy {lvl['PE']} PE Below {p*0.999:.0f}\nSL: {p*1.004:.0f}\n\n⚠️ Risk apna dekh ke Bhai!"
            send(chat_id, txt, main_menu())

        elif "chart" in msg:
            send(chat_id, "📊 <b>Live Chart Links</b>\n\nNifty: https://in.tradingview.com/symbols/NSE-NIFTY/\nBankNifty: https://in.tradingview.com/symbols/NSE-BANKNIFTY/\n\nChart pe 76 level = 100 EMA lagao!", main_menu())

        elif "/help" in msg:
            send(chat_id, "Commands:\n/nifty - Nifty Live\n/banknifty - Bank Live\n/sensex - Sensex\n/finnifty - FinNifty\n/signals - 76 Signal\n/chart - Chart Link", main_menu())

    if "callback_query" in data:
        q = data["callback_query"]
        chat_id = q["message"]["chat"]["id"]
        d = q["data"]
        if d=="nifty":
            p,c,pct = live("^NSEI")
            send(chat_id, f"📈 Nifty: <b>{p:.2f} ({c:+.2f})</b>", main_menu())
        elif d=="bank":
            p,c,pct = live("^NSEBANK")
            send(chat_id, f"🏦 BankNifty: <b>{p:.2f} ({c:+.2f})</b>", main_menu())
        elif d=="signal":
            p,c,pct = live("^NSEI")
            lvl = get_76_levels(p)
            send(chat_id, f"🎯 Signal: CE {lvl['CE']} | PE {lvl['PE']} | Nifty {p:.0f}", main_menu())
        elif d=="chart":
            send(chat_id, "📊 https://in.tradingview.com/symbols/NSE-NIFTY/", main_menu())
        elif d=="sensex":
            p,c,pct = live("^BSESN")
            send(chat_id, f"💹 Sensex: {p:.2f}", main_menu())
        elif d=="finnifty":
            p,c,pct = live("^CNXFIN")
            send(chat_id, f"🔥 FinNifty: {p:.2f}", main_menu())

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
