import requests
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
if not NEWS_API_KEY:
    raise ValueError("NEWS_API_KEY not found in .env file!")

try:
    r = requests.get(f"https://newsapi.org/v2/everything?q=Apple&apiKey={NEWS_API_KEY}", timeout=5)
    print("Connected! Status code:", r.status_code)
    print("Response preview:", r.json().get("articles", [])[:2])  # show 2 articles for testing
except requests.exceptions.Timeout:
    print("Connection timed out.")
except requests.exceptions.RequestException as e:
    print("Failed:", e)
