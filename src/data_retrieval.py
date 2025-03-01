from datetime import date, timedelta
import json
import os
import requests
from dotenv import load_dotenv


def get_data():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    result = {}

    market_data_endpoint = f"{COINGECKO_URL}/coins/markets"
    params = {"vs_currency": "usd", "per_page": 4}
    market_data = requests.get(market_data_endpoint, headers=headers, params=params).json()
    coins_ids_list = [coin['id'] for coin in market_data]

    for coin in market_data:
        result[coin['id']] = {"market data":{k: v for k, v in coin.items() if k != 'id'}}

    for coin_id in coins_ids_list:
        historical_market_chart_by_id_endpoint = f"{COINGECKO_URL}/coins/{coin_id}/market_chart"
        params = {"vs_currency": "usd",
                "days": HISTORY_PERIOD,
                "interval": "daily"}
        history = requests.get(historical_market_chart_by_id_endpoint, headers=headers, params=params).json()
        result[coin_id]["historical data"] = history

    json_result = json.dumps(result)
    return json_result

if __name__ == "__main__":
    load_dotenv()

    COINGECKO_URL = os.getenv("COINGECKO_URL")
    API_KEY = os.getenv("COINGECKO_API_KEY")
    HISTORY_PERIOD = 2 # in days

    if not API_KEY:
        raise ValueError("API key not found. Please check your .env file.")
    
    json_result = get_data()
    print(json_result)