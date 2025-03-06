import os
import requests

# Pushover API credentials (Loaded from GitHub Secrets)
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
PUSHOVER_API_TOKEN = os.getenv("PUSHOVER_API_TOKEN")

# API URL
API_URL = "https://5ztbp1erz4.execute-api.us-east-1.amazonaws.com/v1/campaign"

# API Headers
HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "apikey": os.getenv("API_KEY"),  # Store in GitHub Secrets if required
    "appid": "brnwcs-prod-us-east-1",
    "campaignid": "nJvubTkv",
    "content-type": "application/json",
    "origin": "https://brandnew-live.com",
    "referer": "https://brandnew-live.com/",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36"
}

# Function to check concerts
def check_for_nyc():
    response = requests.get(API_URL, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()  # Parse JSON response

        # Ensure "unique" key exists
        if "message" in data and "unique" in data["message"]:
            concerts = data["message"]["unique"]  # List of concerts
        else:
            print("❌ 'unique' key not found in API response!")
            return

        # Loop through each concert
        for concert in concerts:
            city = concert["venue"]["venueCity"]
            state = concert["venue"]["venueState"]
            venue = concert["venue"]["venueName"]
            ticket_link = concert["venuePurchaseLinks"][0]["link"]

            if "new york" in city.lower() or "brooklyn" in city.lower():
                message = f"🔥 Brand New is coming to {city}, {state} at {venue}! 🎟️ {ticket_link}"
                send_push_notification(message)
                print("✅ NYC/Brooklyn concert found & Push Notification sent!")
                return  # Stop checking after the first match

            # Test for Nashville (for debugging)
            # if "nashville" in city.lower():
            #     message = f"🛠️ [TEST] Brand New is coming to {city}, {state} at {venue}! 🎟️ {ticket_link}"
            #     send_push_notification(message)
            #     print("🛠️ Test Passed: Nashville concert found & Push Notification sent!")
            #     return  # Stop checking after the first match

        print("❌ No NYC/Brooklyn/Nashville concert found.")
    else:
        print(f"⚠️ Failed to fetch API. Status code: {response.status_code} | Response: {response.text[:500]}")

# Function to send Push Notification via Pushover
def send_push_notification(message):
    pushover_url = "https://api.pushover.net/1/messages.json"
    data = {
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "message": message,
        "title": "Brand New Concert Alert!",
        "priority": 1,  # 1 = High priority
    }
    response = requests.post(pushover_url, data=data)
    if response.status_code == 200:
        print("✅ Push Notification sent successfully!")
    else:
        print(f"❌ Failed to send Push Notification. Response: {response.text}")

# Run the check
check_for_nyc()

