import azure.functions as func
import logging
import requests
import os

app = func.FunctionApp()

# ✅ Read env variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ✅ Store last sent slots (in-memory)
last_sent = set()


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        response = requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": msg
        })

        logging.info(f"Telegram status: {response.status_code}")
        logging.info(f"Telegram response: {response.text}")

    except Exception as e:
        logging.error(f"Telegram error: {str(e)}")


@app.timer_trigger(schedule="*/5 * * * *", arg_name="myTimer", run_on_startup=False)
def slotchecker(myTimer: func.TimerRequest) -> None:
    global last_sent

    logging.info("Checking visa slots...")

    # ✅ Debug env variables
    logging.info(f"BOT_TOKEN loaded: {BOT_TOKEN is not None}")
    logging.info(f"CHAT_ID loaded: {CHAT_ID}")

    try:
        url = "https://checkvisaslots.com/latest-us-visa-availability.json"
        response = requests.get(url, timeout=10)

        # ❌ Handle bad response
        if response.status_code != 200 or not response.text.strip():
            logging.error("API returned empty or invalid response")
            return

        data = response.json()

        # ❌ Validate format
        if not isinstance(data, list):
            logging.error("Unexpected API format")
            return

        logging.info(f"API returned {len(data)} records")

        new_slots = []

        for entry in data:
            visa = entry.get("visa_type", "")
            loc = entry.get("location", "")
            date = entry.get("date", "")

            if visa in ["H1B", "H4"]:
                new_slots.append(f"{visa} | {loc} | {date}")

        logging.info(f"Filtered slots count: {len(new_slots)}")

        # ✅ Convert to set
        new_slots_set = set(new_slots)

        # 🔥 Find only NEW slots
        diff = new_slots_set - last_sent

        if diff:
            msg = "🚨 NEW VISA SLOT ALERT 🚨\n\n" + "\n".join(list(diff)[:5])
            send_telegram(msg)

            logging.info("New slots alert sent")

            # ✅ Update memory
            last_sent = new_slots_set

        else:
            logging.info("No NEW slots")

    except Exception as e:
        logging.error(f"Error: {str(e)}")