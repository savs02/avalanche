from flask import Flask, jsonify
from flask_cors import CORS
from crypto_news import CryptoNews
from data_retrieval import CoinData
from previous_trades import PreviousTrades
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/crypto-news", methods=["GET"])
def get_crypto_news():
    news_api = CryptoNews()
    articles = news_api.get_crypto()
    return jsonify([article.to_dict() for article in articles])

@app.route("/market-data", methods=["GET"])
def get_market_data():
    coin_data = CoinData()
    market_data = coin_data.get_data()
    return jsonify(market_data)

@app.get("/trades")
def get_trades():
    prev_trades = PreviousTrades(openai_api_key=os.getenv("OPENAI_API_KEY"))
    trades = prev_trades.get_prev_trades()
    trades.append({"coin":"bitcoin", "price":"87000", "time":"3.10:2:00"})
    if trades:
        return jsonify(trades), 200
        # return {"coin": trade.coin, "price": trade.price, "time": trade.time}
    return jsonify({"detail": "Trade not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
