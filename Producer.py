import requests
from redis import Redis
from rq import Queue
from Tasks import send_email_task
import os
from dotenv import load_dotenv

def get_current_free_games():
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Drill down to the actual list of games
        # Path: data -> Catalog -> searchStore -> elements
        games_list = data.get("data", {}).get("Catalog", {}).get("searchStore", {}).get("elements", [])

        # Find the first game where "isCodeRedemptionOnly" is True
        free_game = next((item for item in games_list if item.get("isCodeRedemptionOnly")), None)

        return free_game
        
    except Exception as e:
        return f"Error fetching data: {e}"

def main():
    load_dotenv()
    game = get_current_free_games()
    if game:
        title = game.get("title")
        print("title sending to redis: ", title)

        #Connect to upstash
        redis_conn = Redis.from_url(os.getenv("REDIS_URL"))

        #Create a queue
        q = Queue(connection=redis_conn)

        recipients = ["20891a1242@gmail.com"]

        for recipient in recipients:
            #Push task into queue
            job = q.enqueue(send_email_task, title, recipient)
            print(f"Sent for {recipient} -> {job.id}")
    else:
        print("No game found")

if __name__=="__main__":
    main()