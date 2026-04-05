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
    print("🔥 VERSION 4 RUNNING 🔥")

    try:
        # ✅ USE WORKING DATA SOURCE (NOT BLOCKED)
        # url = "https://raw.githubusercontent.com/visaslots/data/main/latest.json"
        url = "https://api.github.com/repos/visaslots/data/contents"

        response = requests.get(url, timeout=10)

        print("Status:", response.status_code)

        if response.status_code != 200:
            print("API failed")
            return

        # data = response.json()

        # print("Records:", len(data))

        # msg = "🚨 TEST ALERT 🚨\n\n"

        # for entry in data[:5]:
        #     msg += f"{entry.get('visa_type')} | {entry.get('location')} | {entry.get('date')}\n"

        msg = "🚨 TEST ALERT 🚨\n\nGitHub API working ✅"
        send_telegram(msg)

        send_telegram(msg)

    except Exception as e:
        print("Error:", str(e))


# 🔁 RUN LOOP
while True:
    check_slots()
    time.sleep(300)