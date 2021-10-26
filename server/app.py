COURSES = [
    {
        'title': 'Effective JavaScript: 68 Specific Ways to Harness the Power of JavaS                   cript ',
        'author': 'David Herman',
        'paperback': True
    },
    {
        'title': 'JavaScript: The Good Parts',
        'author': 'Douglas Crockford',
        'paperback': False    
    },
    {
        'title': 'Eloquent JavaScript: A Modern Introduction to Programming',
        'author': 'Marijn Haverbeke',
        'paperback': True
    }
]    

from flask import Flask, jsonify
import requests
from pprint import pprint
from functions import marketMethods
from config import get_config

app = Flask(__name__)
CONFIG = get_config()

@app.route('/courses', methods=['GET'])
def all_courses():
    response = jsonify({
        'status': 'success',
        'courses': COURSES
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/market', methods=['GET'])
def top_ten_markets():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
    try:
        response = requests.get(url)
        response.raise_for_status()
        #Return the top 10 markets
        response = jsonify({
        'status': 'success',
        'markets': response.json()[:CONFIG.TOP_CURRENCY_COUNT]
        })
        #pprint(marketMethods.topTen(response.json))
        return response
    except HTTPError as http_err:
        print(f'HTTPS error occured: {http_err}')
        return http_err
    except Exception as err:
        print(f'An Error Occured: {err}')
    return response