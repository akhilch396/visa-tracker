import requests
import os

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
    print("🔥 VERSION FINAL (GITHUB ACTIONS) 🔥")

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
            print("No slots found")
            return

        msg = "🚨 VISA SLOTS FOUND 🚨\n\n"

        for entry in data[:5]:
            msg += f"{entry}\n"

        send_telegram(msg)

    except Exception as e:
        print("Error:", str(e))


# ✅ RUN ONLY ONCE (IMPORTANT FOR GITHUB ACTIONS)
if __name__ == "__main__":
    check_slots()