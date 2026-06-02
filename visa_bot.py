from playwright.sync_api import sync_playwright
import requests
import time

BOT_TOKEN = "8984169652:AAHJVu9IExEkBcaP33GUYID BCxqoHqHvWWI"
CHAT_ID = "7030989155"

URL = "https://broneering.mfa.ee/en/"

def send_telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )

def check_appointments():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL, timeout=60000)

        # Wait for page to fully load
        page.wait_for_timeout(5000)

        content = page.content()

        browser.close()

        # Basic detection logic (we will refine)
        keywords = [
            "No appointments",
            "no available",
            "fully booked"
        ]

        if not any(k.lower() in content.lower() for k in keywords):
            send_telegram("🚨 VISA APPOINTMENT POSSIBLY AVAILABLE!\nCheck now: " + URL)
        else:
            print("No slots found")

while True:
    try:
        check_appointments()
    except Exception as e:
        print("Error:", e)

    time.sleep(120)  # every 2 minutes
