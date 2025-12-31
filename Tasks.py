import requests
import os
from dotenv import load_dotenv

# load_dotenv() is good for local testing, but GitHub Actions will use env secrets
load_dotenv()

def send_ntfy_notification(game_title, url):
    topic = os.getenv("NTFY_TOPIC")
    
    if not topic:
        print("❌ Error: NTFY_TOPIC environment variable is missing!")
        return

    response = requests.post(
        f"https://ntfy.sh/{topic}",
        data=f"Grab it now: {game_title}",
        headers={
            "Title": "🎮 Epic Games Freebie Alert!",
            "Priority": "high",
            "Tags": "video_game,gift",
            "Click": url,   
            # Added f"" below so {url} correctly inserts the game link
            "Actions": f"view, Open Store, {url}" 
        }
    )

    if response.status_code == 200:
        print(f"✅ Notification for '{game_title}' sent to topic: {topic}")
    else:
        print(f"❌ Failed to send. Status code: {response.status_code}")