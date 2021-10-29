from flask import Flask, jsonify, request
import requests
from pprint import pprint
from config import get_config
from flask_cors import CORS
import pymongo
import bcrypt

from functions.database import Database
from functions.User import User

app = Flask(__name__)
CORS(app)
CONFIG = get_config()
client = pymongo.MongoClient(CONFIG.DB_URI)
Database.initialize(CONFIG.DB_URI)

@app.route('/api/market', methods=['GET'])
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
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except HTTPError as http_err:
        print(f'HTTPS error occured: {http_err}')
        return http_err
    except Exception as err:
        print(f'An Error Occured: {err}')
        return err
@app.route('/api/register', methods=['POST'])
def user_registration():
    data = request.json
    print(data)
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    username_exists = Database().check_username_exists(data['username'])
    print(username_exists)
    if username_exists:
        response = jsonify({
        'status':'username already exists'
        })
        return response
    new_user = User(data['username'], hashed_password)
    Database().insert_new_user(new_user.return_query_data())
    if bcrypt.checkpw(data['password'].encode('utf-8'), hashed_password):
        print("Password MATCH!")
    print(new_user.return_query_data())
    response = jsonify({
        'status':'success'
        
    })
    return response



sample = {
    "username":"Beb",
    "password":"Bobz",
    "balance": "2000",
    "assets": {"BTC": "1000"}
}
def test(data):
    testUser = User("Beb", "Apple")
    testUser2 = User(sample['username'], sample['password'], sample['balance'], sample['assets'])
    print(testUser.return_query_data())
    print(testUser2.return_query_data())
    cursor = Database.find()
    for doc in cursor:
        print(doc)


test(sample)