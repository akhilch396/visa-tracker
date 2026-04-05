import requests
import os
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_telegram(msg):
    url = f"https://api.telegram.org/bot8637487298:AAFmDtvyk-ky-i2OZ6FtvpXQ1niVehWdhAo/sendMessage"
    res = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })
    print("Telegram:", res.status_code, res.text)


def check_slots():
    print("🔥 VERSION 5 RUNNING (FINAL TEST) 🔥")

    # ✅ JUST SEND MESSAGE (NO API)
    msg = "🚨 SYSTEM WORKING 🚨\n\nYour visa tracker is running successfully!"

    send_telegram(msg)


# 🔁 RUN EVERY 5 MINUTES
while True:
    check_slots()
    time.sleep(300)