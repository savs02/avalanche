import os
import requests
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("CRYPTO_NEWS_API_KEY")
url = "https://cryptonews-api.com/api/v1"

params = {
    "tickers": "BTC,ETH,XRP",  # Bitcoin, Ethereum, and Ripple tickers
    "items": 3,              
    "page" : 1, # Number of news items you want to retrieve
    "token": API_KEY,
}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an error for bad responses
    news_data = response.json()

    # Check if the API returned news articles under the 'data' key.
    articles = news_data.get("data", [])
    if not articles:
        print("No news articles found.")
    else:
        for article in articles:
            # Each article is a dictionary with keys like 'title', 'publishedAt', 'source', and 'url'.
            print(f"Title: {article.get('title')}")
            print(f"Published At: {article.get('date')}")
            print(f"URL: {article.get('news_url')}")
            print(article.get('text'))
            print("-" * 50)
except requests.RequestException as e:
    print("Error fetching news:", e)
