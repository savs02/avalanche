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

    def to_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "source": "CryptoNews",
            "publishedAt": self.date,
            "urlToImage": self.image
        }

class CryptoNews:
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv("CRYPTO_NEWS_API_KEY")
        self.url = "https://cryptonews-api.com/api/v1"
        self.params = {
            "tickers": "BTC,ETH,XRP",
            "items": 3,
            "page": 1, 
            "token": self.API_KEY,
        }

    def get_crypto(self):
        response = requests.get(self.url, params=self.params)
        response.raise_for_status()
        news_data = response.json()

        result = []
        articles = news_data.get("data", [])
        
        for article in articles:
            article_obj = Article(
                article.get('title'),
                article.get('date'),
                article.get('news_url'),
                article.get('text'),
                article.get('image_url')
            )
            result.append(article_obj)
        
        return result
