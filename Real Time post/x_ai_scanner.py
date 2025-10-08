import tweepy
import time
import csv
from schedule import every, repeat, run_pending
import keyboard  # New import for key detection

# X API credentials (replace with your own)
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_TOKEN_SECRET = "your_access_token_secret"

# Authenticate with X API
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# CSV file setup
CSV_FILE = "x_ai_posts.csv"
FIELDNAMES = ["timestamp", "username", "post_text"]
MAX_USERS = 10
MAX_POSTS = 10

def init_csv():
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        if file.tell() == 0:
            writer.writeheader()

def fetch_x_posts():
    print(f"Fetching recent posts with #AI at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    unique_users = set()
    posts_data = []
    try:
        tweets = api.search_tweets(q="#AI", lang="en", result_type="recent", count=100)
        for tweet in tweets:
            if len(posts_data) >= MAX_POSTS:
                break
            username = tweet.user.screen_name
            post_text = tweet.text
            timestamp = tweet.created_at.strftime("%Y-%m-%d %H:%M:%S")
            if len(unique_users) < MAX_USERS and username not in unique_users:
                unique_users.add(username)
                posts_data.append({"timestamp": timestamp, "username": username, "post_text": post_text})
            elif username in unique_users:
                posts_data.append({"timestamp": timestamp, "username": username, "post_text": post_text})
        with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            for post in posts_data:
                writer.writerow(post)
        print(f"Saved {len(posts_data)} posts from {len(unique_users)} users.")
    except tweepy.TweepyException as e:
        print(f"Error fetching posts: {e}")

@repeat(every(5).minutes)
def job():
    fetch_x_posts()

if __name__ == "__main__":
    init_csv()
    print("Starting X post scanner for #AI... Press 'q' to stop.")
    while True:
        run_pending()
        time.sleep(1)
        if keyboard.is_pressed("q"):  # Check if 'q' is pressed
            print("Stopping the scanner...")
            break