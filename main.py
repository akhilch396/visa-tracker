import requests
import os
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

last_sent = set()  # prevents duplicate alerts


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    res = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })

    print("Telegram:", res.status_code)


def check_slots():
    global last_sent

    print("🔥 VERSION 8 RUNNING (REAL TRACKER) 🔥")

    try:
        url = "https://api.github.com/repos/saransh138/h1b-visa-slots/contents/slots.json"

        headers = {
            "Accept": "application/vnd.github.v3.raw"
        }

        response = requests.get(url, headers=headers)

        print("Status:", response.status_code)

        if response.status_code != 200:
            print("API failed")
            return

        data = response.json()

        if not data:
            print("No slots available")
            return

        new_slots = []

        for entry in data:
            text = str(entry)

            if text not in last_sent:
                new_slots.append(text)

        if not new_slots:
            print("No new slots")
            return

        msg = "🚨 NEW VISA SLOTS 🚨\n\n"

        for slot in new_slots[:5]:
            msg += f"{slot}\n"

        send_telegram(msg)

        last_sent.update(new_slots)

    except Exception as e:
        print("Error:", str(e))


while True:
    check_slots()
    time.sleep(300)