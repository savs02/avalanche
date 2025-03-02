import os
import openai
from dotenv import load_dotenv

class Trade:
    def __init__(self, coin, price, time):
        self.coin = coin
        self.price = price
        self.time = time

class PreviousTrades:
    def __init__(self, openai_api_key, model="gpt-4"):
        self.trades = {}
        self.model = model 
        openai.api_key = openai_api_key

    def add_trade(self, text, coin, price, time):
        key_words = self.get_keys(text)
        key = '@'.join(key_words)
        self.trades[key] = Trade(coin, price, time)

    def get_keys(self, text):
        prompt = (
            "Find the most relevant keywords based on the following text, separated by commas:\n\n"
            f"{text}\n\n"
            "Keywords:"
        )
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts keywords from text."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.5,
                max_tokens=60,
            )
            keywords_str = response.choices[0].message.content.strip()
            keywords = [kw.strip() for kw in keywords_str.split(',') if kw.strip()]
            return keywords
        except Exception as e:
            print("Error while extracting keywords:", e)
            return [word.lower() for word in text.split() if len(word) > 3]

    def get_trade(self, text):
        key_words = self.get_keys(text)
        for key, trade in self.trades.items():
            stored_keywords = key.split("@")
            freq = sum(1 for word in stored_keywords if word in key_words)
            if len(key_words) > 0 and (freq / len(key_words)) >= 0.5:
                return trade
        return None


if __name__ == "__main__":
    load_dotenv()
    trades_db = PreviousTrades(openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4")
    trades_db.add_trade("sell me something victoria", "BTC", 50000, "2025-03-01 12:00")
    trade = trades_db.get_trade("victoria is selling something")
    if trade:
        print(f"Found trade: {trade.coin} at {trade.price}")
    else:
        print("No matching trade found.")
