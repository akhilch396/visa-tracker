import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        response = requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": msg
        })

        print(f"Telegram status: {response.status_code}")
        print(f"Telegram response: {response.text}")

    except Exception as e:
        print(f"Telegram error: {str(e)}")


def check_slots():
    print("🔥 VERSION 2 DEPLOYED 🔥")
    print("Checking visa slots...")

    try:
        url = "https://checkvisaslots.com/latest-us-visa-availability.json"
        response = requests.get(url, timeout=10)

        # ✅ Log API response info
        print(f"API status: {response.status_code}")
        print(f"API response sample: {response.text[:200]}")

        # ❌ Handle bad response
        if response.status_code != 200:
            print("API error: bad status code")
            return

        if not response.text.strip():
            print("API error: empty response")
            return

        # ❌ Handle invalid JSON
        try:
            data = response.json()
        except Exception:
            print("API error: invalid JSON")
            return

        if not isinstance(data, list):
            print("API error: unexpected format")
            return

        print(f"Records received: {len(data)}")

        slots = []

        for entry in data:
            visa = entry.get("visa_type", "")
            loc = entry.get("location", "")
            date = entry.get("date", "")

            if visa in ["H1B", "H4"]:
                slots.append(f"{visa} | {loc} | {date}")

        # 🔥 Send alert if slots exist
        if slots:
            msg = "🚨 VISA SLOT ALERT 🚨\n\n" + "\n".join(slots[:5])
            send_telegram(msg)
            print("✅ Alert sent")
        else:
            print("No slots found")

    except Exception as e:
        print(f"ERROR: {str(e)}")


# 🔁 Run every 5 minutes (300 sec)
while True:
    check_slots()
    time.sleep(300)