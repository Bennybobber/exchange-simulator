from flask import Flask, jsonify, request, make_response
import requests

from flask_cors import CORS
import pymongo
import bcrypt
import jwt
import uuid
import datetime
from functools import wraps

from config import get_config
from functions.database import Database
from functions.User import User

app = Flask(__name__)
app.config['SECRET_KEY']='Th1s1ss3cr3t'
CORS(app)
CONFIG = get_config()
client = pymongo.MongoClient(CONFIG.DB_URI)
Database.initialize(CONFIG.DB_URI)

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config[SECRET_KEY])
            current_user = Database().find_one(data['public_id'])
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)
   return decorator

@app.route('/register', methods=['POST'])
def user_registration():
    data = request.json
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    username_exists = Database().check_username_exists(data['username'])
    if username_exists:
        response = jsonify({
        'status':'username already exists'
        })
        return response
    new_user = User(data['username'], hashed_password)
    Database().insert_new_user(new_user.return_query_data())
    #if bcrypt.checkpw(data['password'].encode('utf-8'), hashed_password):
    response = jsonify({
        'status':'successfully registered user'
        
    })
    return response

@app.route('/login', methods=['POST'])  
def login_user(): 
 
    auth = request.json   
    print(auth)
    if not auth or not auth['username'] or not auth['password']:  
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

    username_exists = Database().check_username_exists(auth['username'])
    if username_exists:
        if bcrypt.checkpw(auth['password'].encode('utf-8'), Database().retrieve_hashed_password(auth['username'])):  
            token = jwt.encode({
                'public_id': auth['username'],
                'iat':datetime.datetime.utcnow(),
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                app.config['SECRET_KEY'])  
            return jsonify({'accessToken' : token, 'id': auth['username']}) 

    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

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
    cursor = Database.find()
    for doc in cursor:
        print(doc)

test(sample)