import os
import requests
from dotenv import load_dotenv

class Article:
    def __init__(self, title, date, url, text, image):
        self.title = title
        self.date = date
        self.url = url
        self.text = text
        self.image = image


class CryptoNews:
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv("CRYPTO_NEWS_API_KEY")
        self.url = "https://cryptonews-api.com/api/v1"
        self.params = {
                "tickers": "BTC,ETH,XRP", 
                "items": 3,              
                "page" : 1, 
                "token": self.API_KEY,
            }
        
    def get_crypto(self):
        response = requests.get(self.url, params=self.params)
        response.raise_for_status()  
        news_data = response.json()
        result = []

        articles = news_data.get("data", [])
        if not articles:
            print("No news articles found.")
        else:
            for article in articles:
                result.append(Article(article.get('title'), article.get('date'), article.get('news_url'), article.get('text'), article.get('image_url')))
        return result
