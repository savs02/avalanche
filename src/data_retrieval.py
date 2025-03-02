from datetime import date, timedelta
import json
import os
import requests
from dotenv import load_dotenv


class CoinData:
    def __init__(self):
        load_dotenv()
        self.COINGECKO_URL = os.getenv("COINGECKO_URL")
        self.API_KEY = os.getenv("COINGECKO_API_KEY")
        self.HISTORY_PERIOD = 2 # in days
        self.result = None

    def get_data(self):
        headers = {
            "Authorization": f"Bearer {self.API_KEY}",
            "Content-Type": "application/json"
        }

        result = {}

        market_data_endpoint = f"{self.COINGECKO_URL}/coins/markets"
        params = {"vs_currency": "usd", "per_page": 4}
        market_data = requests.get(market_data_endpoint, headers=headers, params=params).json()
        coins_ids_list = [coin['id'] for coin in market_data]

        for coin in market_data:
            result[coin['id']] = {"market data":{k: v for k, v in coin.items() if k != 'id'}}

        for coin_id in coins_ids_list:
            historical_market_chart_by_id_endpoint = f"{self.COINGECKO_URL}/coins/{coin_id}/market_chart"
            params = {"vs_currency": "usd",
                    "days": self.HISTORY_PERIOD,
                    "interval": "daily"}
            history = requests.get(historical_market_chart_by_id_endpoint, headers=headers, params=params).json()
            result[coin_id]["historical data"] = history

        json_result = json.dumps(result)
        self.result = json_result
        return json_result
    
    def get_result(self):
        return self.result