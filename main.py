import requests
import os
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    res = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })

    print("Telegram:", res.status_code, res.text)


def check_slots():
    print("🔥 VERSION 7 RUNNING (FINAL CHECK) 🔥")

    try:
        url = "https://api.github.com/repos/saransh138/h1b-visa-slots/contents/slots.json"

        headers = {
            "Accept": "application/vnd.github.v3.raw"
        }

        response = requests.get(url, headers=headers)

        print("Status:", response.status_code)

        # ✅ TEST MODE (FOR NOW)
        msg = "🚨 TEST SUCCESS 🚨\n\nTracker is running on Railway!"

        send_telegram(msg)

    except Exception as e:
        print("Error:", str(e))


# 🔁 LOOP
while True:
    check_slots()
    time.sleep(300)