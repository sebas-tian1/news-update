from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get('NEWS_API_KEY', 'Your_News_API_Key')
BASE_URL = 'https://newsapi.org/v2/top-headlines'

def fetch_news(country: str, page: int, page_size: int):
    params = {
        'category': 'business',
        'country': country,
        'page': page,
        'pageSize': page_size,
        'apiKey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        return {'error': 'Failed to fetch news'}, response.status_code
    news_data = response.json()
    return {
        'page': page,
        'page_size': page_size,
        'total': news_data.get('totalResults', 0),
        'news': news_data.get('articles', [])
    }

@app.route('/news/global')
def global_news():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    result = fetch_news('us', page, page_size)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

