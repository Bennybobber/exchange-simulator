from flask import Flask, jsonify, request, make_response
import requests

from flask_cors import CORS
import pymongo
import bcrypt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    create_refresh_token,
    get_jwt_identity
)
from bson import json_util, ObjectId
import json

from config import get_config
from functions.database import Database
from functions.User import User

app = Flask(__name__)
jwt = JWTManager(app)
app.config['SECRET_KEY']='Th1s1ss3cr3t'
CORS(app)
CONFIG = get_config()
client = pymongo.MongoClient(CONFIG.DB_URI)
Database.initialize(CONFIG.DB_URI)

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
        'message':'successfully registered user'
        
    })
    return response

@app.route('/login', methods=['POST'])  
def login_user(): 
    auth = request.json   
    if not auth or not auth['username'] or not auth['password']:  
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

    username_exists = Database().check_username_exists(auth['username'])
    if username_exists:
        if bcrypt.checkpw(auth['password'].encode('utf-8'), Database().retrieve_hashed_password(auth['username'])):  
            # token = jwt.encode({
            #     'public_id': auth['username'],
            #     'iat':datetime.datetime.utcnow(),
            #     'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            #     app.config['SECRET_KEY'])
            ret = {
                'accessToken': create_access_token(identity=auth['username']),
                'refreshToken': create_refresh_token(identity=auth['username']),
            }  
            return jsonify(ret), 200 

    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

@app.route('/refreshtoken', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    print("hello")
    current_user = get_jwt_identity() 
    ret = {
        'accessToken': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200

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

@app.route('/api/user', methods=['GET'])
@jwt_required()
def retrieve_user_data():
    username = get_jwt_identity()
    query = {
            "username":username
        }
    user_data=Database().find_one(query)
    print(user_data)
    user_data = json.dumps(user_data, default=str)
    return user_data, 200
    # return jsonify(logged_in_as=username), 200
    

