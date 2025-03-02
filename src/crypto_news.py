import os
import requests
from dotenv import load_dotenv

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
        output_string_arr = []

        articles = news_data.get("data", [])
        if not articles:
            print("No news articles found.")
        else:
            for article in articles:
                result.append({'title': article.get('title'), 
                            'date': article.get('date'), 
                            'news_url': article.get('news_url'), 
                            'text': article.get('text'), 
                            'image_url': article.get('image_url')
                            })
                output_string_arr.append(
                                f"Title: {article.get('title')}\n"
                                f"Date: {article.get('date')}\n"
                                f"URL: {article.get('news_url')}\n"
                                f"Text: {article.get('text')}\n"
                                + "-" * 30
                            )
        return result, output_string_arr
