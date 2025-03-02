from flask import Flask, jsonify
from flask_cors import CORS
from crypto_news import CryptoNews
from data_retrieval import CoinData

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

if __name__ == "__main__":
    app.run(debug=True)
