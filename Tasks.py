import requests
import os
from dotenv import load_dotenv

load_dotenv()

def send_ntfy_notification(game_title, url):
    topic = os.getenv("NTFY_TOPIC")
    if not topic:
        print("❌ Error: NTFY_TOPIC environment variable is missing!")
        return

    # We removed the 🎮 emoji from the "Title" header to avoid the Latin-1 error
    response = requests.post(
        f"https://ntfy.sh/{topic}",
        data=f"🎮 Free Game: {game_title}", # Emojis are OK here in the body!
        headers={
            "Title": "Epic Games Freebie Alert", # Plain text only here
            "Priority": "high",
            "Tags": "video_game,gift",
            "Click": url,   
            "Actions": f"view, Open Store, {url}" 
        }
    )

    if response.status_code == 200:
        print(f"✅ Notification sent successfully to {topic}")
    else:
        print(f"❌ Failed to send. Status code: {response.status_code}")