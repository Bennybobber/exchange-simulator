from flask import Flask, jsonify, request, make_response
import time

from flask_cors import CORS
import asyncio
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
from models.database import Database
from models.User import User
from functions import marketMethods

app = Flask(__name__)
jwt = JWTManager(app)
CORS(app)
CONFIG = get_config()
app.config['SECRET_KEY']=CONFIG.SECRET_KEY
client = pymongo.MongoClient(CONFIG.DB_URI)
Database.initialize(CONFIG.DB_URI)
api_key = CONFIG.COIN_API_KEY
loop = asyncio.get_event_loop()

@app.route('/register', methods=['POST'])
async def user_registration():
    """
    user_registration registers a new user in the mongo database by taking username and password
    uses bycrpyt to hash and salt the password before storing in the db.

    :return: returns a response to say a user was successfully registered, the name was taken
    or an unknown other error has occured.
    """
    try:
        data = request.json
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        username_exists = await Database().check_username_exists(data['username'])
        if username_exists:
            return make_response('Username already exists',  403)
        new_user = User(data['username'], hashed_password)
        await Database().insert_new_user(new_user.return_query_data())
        response = jsonify({
            'message':'successfully registered user'
        
        })
        return response, 201
    except Exception as err:
        return make_response('Unknown Error Has Occured',  500)

    

@app.route('/login', methods=['POST'])  
async def login_user():
    """
    login_user takes in request params Username and Password and checks them against the database stored ones.

    :return: returns a response to say a user was successfully logged in, that the credentials could not be
    verified or an unknown other error has occured.
    """
    try: 
        auth = request.json
        if not auth or not auth['username'] or not auth['password']:  
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

        username_exists = await Database().check_username_exists(auth['username'])
        if username_exists:
            if bcrypt.checkpw(auth['password'].encode('utf-8'), await Database().retrieve_hashed_password(auth['username'])):
                ret = {
                    'accessToken': create_access_token(identity=auth['username']),
                    'refreshToken': create_refresh_token(identity=auth['username']),
                }
                return jsonify(ret), 200 
        return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})
    except Exception as err:
        return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})
    
@app.route('/refreshtoken', methods=['POST'])
@jwt_required(refresh=True)
async def refresh():
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
async def markets():
    """
    Retrieves the top markets that match both coinapi and coingeckos so the data can be used
    to get both information about the asset (from coingecko) and market information and ids
    (from coinapi). 

    :return: Returns a dictionary of the top 100 cryptocurrnecy markets, or a 500 error for an
    unknown error.

    """
    try:
        markets = await marketMethods.getTradablePairs()
        response = jsonify({
        'status': 'success',
        'markets': markets
        })
        return response, 200
    except Exception as err:
        print(f'An Error Occured: {err}')
        return jsonify({'message': 'An Unknown Error Has Occured'}), 500
    return jsonify({'message': 'An Unknown Error Has Occured'}), 500

@app.route('/api/user', methods=['GET','PUT','DELETE'])
@jwt_required()
async def retrieve_user_data():
    """
    retrieve_user_data calls a function in the Database module to retrieve the users details
    for their portfolio page. 

    :return: Returns a dictionary of the users information, a 401 error if they're not authorized
    and a 500 if an unknown error has occured.

    """
    if request.method == 'GET':
        try:
            user_data = await Database().retrieve_user_portfolio(get_jwt_identity())
            user_data = json.dumps(user_data, default=str)
            return user_data, 200
        except Exception as err:
            return jsonify({'message': 'An Unknown Error Has Occured'}), 500
    if request.method == 'PUT':
        try:
            await Database().update_user(request.json['data'])
            return jsonify({'message':'Successful Trade'}), 200
        except Exception as err:
            print(err)
            return jsonify({'message': 'An Unknown Error Has Occured'}), 500
    if request.method == 'DELETE':
        try:
            await Database().delete_user(get_jwt_identity())
            return jsonify({'message':'Successful deletion'}), 200
        except Exception as err:
            print(err)
            return jsonify({'message': 'An Unknown Error Has Occured'}), 500
    
@app.route('/api/pairs', methods=['GET'])
async def retrieve_coinApi_pairs():
    """
    This retrieves all the tradable pairs (Ones that both match coingecko and coinapi).

    :return: Returns a dictionary of all the tradable pairs, or a 500 error for an
    unknown error.

    """
    try:
        return jsonify({"coins": await marketMethods.getTradablePairs()}), 200
    except Exception as err:
        return jsonify({'message': 'An Unknown Error Has Occured'}), 500 

@app.route('/api/coin/info', methods=['GET'])
async def get_coin_information():
    """
    Retrieves a specific coins information.

    :return: Returns a dictionary with the details of a specific assset,
    a 404 for unknown coin, or a 500 error for an unknown error.

    """
    try:
        data = await marketMethods.specific_coin(request.args.get('symbol'))
        if data is False:
            return jsonify({'message': 'Coin was not found'}), 404
        return jsonify(data), 200
    except Exception as err:
        return jsonify({'error': err}), 500

@app.route('/api/coin/history', methods=['GET'])
async def get_coin_history():
    """
    Retrieves the candlestick history for a given coin asset.

    :params:
        args.get('coin') (String): a string of the coins ID
        args.get('interval') (String): an interval of history

    :return: Returns a dictionary of candlestick data given in the current
    interval sent, or a 500 error if an error occurs.

    """
    data  = None
    try:
        data = await marketMethods.get_coin_history(request.args.get('coin'), request.args.get('interval'))
        while (type(data) != dict):
            time.sleep(5)
            data = await marketMethods.get_coin_history(request.args.get('coin'), request.args.get('interval'))
        return data, 200
    except Exception as err:
        print(err)
        return jsonify({'error': err}), 500

if __name__ == '__main__':
    app.run(debug=True)