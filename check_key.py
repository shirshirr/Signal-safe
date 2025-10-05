import os
from dotenv import load_dotenv

load_dotenv()  # load .env from current folder

print("NEWS_API_KEY:", os.getenv("NEWS_API_KEY"))
