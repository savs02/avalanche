from flask import Flask, jsonify
from flask_cors import CORS
from crypto_news import CryptoNews

app = Flask(__name__)
CORS(app)

@app.route("/crypto-news", methods=["GET"])
def get_crypto_news():
    news_api = CryptoNews()
    articles = news_api.get_crypto()
    return jsonify([article.to_dict() for article in articles])

if __name__ == "__main__":
    app.run(debug=True)
