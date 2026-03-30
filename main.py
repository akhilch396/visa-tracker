import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

last_sent = set()

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def check_slots():
    global last_sent

    print("Checking visa slots...")

    try:
        url = "https://checkvisaslots.com/latest-us-visa-availability.json"
        response = requests.get(url, timeout=10)

        if response.status_code != 200 or not response.text.strip():
            print("API error")
            return

        data = response.json()

        new_slots = []

        for entry in data:
            visa = entry.get("visa_type", "")
            loc = entry.get("location", "")
            date = entry.get("date", "")

            if visa in ["H1B", "H4"]:
                new_slots.append(f"{visa} | {loc} | {date}")

        new_slots_set = set(new_slots)
        diff = new_slots_set - last_sent

        if diff:
            msg = "🚨 NEW VISA SLOT ALERT 🚨\n\n" + "\n".join(list(diff)[:5])
            send_telegram(msg)
            print("Alert sent")

            last_sent = new_slots_set
        else:
            print("No new slots")

    except Exception as e:
        print("Error:", e)


while True:
    check_slots()
    time.sleep(300)  # every 5 mins