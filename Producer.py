import requests
from redis import Redis
from rq import Queue
from Tasks import send_ntfy_notification # Updated function name
import os
from dotenv import load_dotenv

def get_current_free_games():
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        games_list = data.get("data", {}).get("Catalog", {}).get("searchStore", {}).get("elements", [])

        # Find the game currently free (usually has a discounted price of 0)
        # Or keep your specific filter if you only want code-redemption games
        free_game = next((item for item in games_list if item.get("isCodeRedemptionOnly")), None)
        
        # Fallback: If no "code" game, get the first actual free game
        if not free_game:
            free_game = games_list[0] if games_list else None

        return free_game
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def main():
    if os.path.exists(".env"):
        load_dotenv()
    
    game = get_current_free_games()
    if game:
        title = game.get("title")
        
        # Generate the Epic Store URL
        # Path: catalogNs -> mappings -> pageSlug
        try:
            slug = game.get("catalogNs", {}).get("mappings", [{}])[0].get("pageSlug")
            game_url = f"https://store.epicgames.com/en-US/p/{slug}"
        except:
            game_url = "https://store.epicgames.com/en-US/free-games"

        print(f"Game found: {title}. Sending to Redis...")

        url = os.getenv("REDIS_URL")
        if url:
            url = url.strip() 

        redis_conn = Redis.from_url(url)
        q = Queue(connection=redis_conn)
        
        # Enqueue the task with title and the URL
        job = q.enqueue(send_ntfy_notification, title, game_url)
        print(f"✅ Job enqueued successfully: {job.id}")
    else:
        print("No game found today.")

if __name__=="__main__":
    main()