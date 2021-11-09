from flask import Flask, jsonify, request, make_response
import requests
import time

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
from functions import marketMethods


app = Flask(__name__)
jwt = JWTManager(app)
app.config['SECRET_KEY']='Th1s1ss3cr3t'
CORS(app)
CONFIG = get_config()
client = pymongo.MongoClient(CONFIG.DB_URI)
Database.initialize(CONFIG.DB_URI)
api_key = CONFIG.COIN_API_KEY

@app.route('/register', methods=['POST'])
def user_registration():
    """
    user_registration registers a new user in the mongo database by taking username and password
    uses bycrpyt to hash and salt the password before storing in the db.

    :return: returns a response to say a user was successfully registered, the name was taken
    or an unknown other error has occured.
    """
    try:
        data = request.json
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        username_exists = Database().check_username_exists(data['username'])
        if username_exists:
            response = jsonify({
            'status':'Username already exists'
            })
            return response, 403
        new_user = User(data['username'], hashed_password)
        Database().insert_new_user(new_user.return_query_data())
        response = jsonify({
            'message':'successfully registered user'
        
        })
        return response, 201
    except Exception as err:
        return jsonify({'message': 'An Unknown Error Has Occured'}), 500

    

@app.route('/login', methods=['POST'])  
def login_user():
    """
    login_user takes in request params Username and Password and checks them against the database stored ones.

    :return: returns a response to say a user was successfully logged in, that the credentials could not be
    verified or an unknown other error has occured.
    """
    try: 
        auth = request.json   
        if not auth or not auth['username'] or not auth['password']:  
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

        username_exists = Database().check_username_exists(auth['username'])
        if username_exists:
            if bcrypt.checkpw(auth['password'].encode('utf-8'), Database().retrieve_hashed_password(auth['username'])):  
                ret = {
                    'accessToken': create_access_token(identity=auth['username']),
                    'refreshToken': create_refresh_token(identity=auth['username']),
                }  
                return jsonify(ret), 200 
    except Exception as err:
        return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})
    
@app.route('/refreshtoken', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    refresh checks the incoming authorization header for a valid refresh token and then returns a new access
    token to the user.

    :return: returns new access token, or an 401 for an invalid token

    """
    current_user = get_jwt_identity() 
    ret = {
        'accessToken': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200

@app.route('/api/market', methods=['GET'])
def top_ten_markets():
    """
    top_ten_markets does an API GET request to the coingecko PUBLIC API to retrieve the markets
    and filters out the to the top 10. 

    :return: Returns a dictionary of the top 10 cryptocurrnecy markets, or a 500 error for an
    unknown error.

    """
    try:
        #Return the top 10 markets
        response = jsonify({
        'status': 'success',
        'markets': marketMethods.getTradablePairs()[:CONFIG.TOP_CURRENCY_COUNT]
        })
        return response, 200
    except HTTPError as http_err:
        print(f'HTTPS error occured: {http_err}')
        return http_err, 500
    except Exception as err:
        print(f'An Error Occured: {err}')
        return jsonify({'message': 'An Unknown Error Has Occured'}), 500

@app.route('/api/user', methods=['GET'])
@jwt_required()
def retrieve_user_data():
    """
    retrieve_user_data calls a function in the Database module to retrieve the users details
    for their portfolio page. 

    :return: Returns a dictionary of the users information, a 401 error if they're not authorized
    and a 500 if an unknown error has occured.

    """
    try:
        username = get_jwt_identity()
        user_data=Database().retrieve_user_portfolio(username)
        user_data = json.dumps(user_data, default=str)
        return user_data, 200
    except Exception as err:
        return jsonify({'message': 'An Unknown Error Has Occured'}), 500
    
@app.route('/api/pairs', methods=['GET'])
def retrieve_binance_pairs():
    try:
        return jsonify({"coins": marketMethods.getTradablePairs()}), 200
    except Exception as err:
        return jsonify({'message': 'An Unknown Error Has Occured'}), 500 

@app.route('/api/coin/info', methods=['GET'])
def get_coin_information():
    try:
        data = marketMethods.specific_coin(request.args.get('symbol'))
        return jsonify(data), 200
    except Exception as err:
        return jsonify({'error': err}), 500
@app.route('/api/coin/history', methods=['GET'])
def get_coin_history():
    try:
        data = marketMethods.get_coin_history(request.args.get('coin'), request.args.get('interval'))
        return data, 200
    except Exception as err:
        print(err)
        return jsonify({'error': err}), 500