import pymongo
import bcrypt

class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None
    user_collection = 'user_accounts'

    @staticmethod
    def initialize(URI):
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['SimEx']
    

    @staticmethod
    def insert_new_user(data):
        #hashedData = encrypt_data(Database.user_collection)
        Database.DATABASE[Database.user_collection].insert(data)
    @staticmethod
    def update_user(data):
        query = {
            "username": data['username']
        }
        currentUser = Database().find_one(query)
        Database.DATABASE[Database.user_collection].replace_one(query, data)

    @staticmethod
    def find():
        return Database().DATABASE[Database.user_collection].find()

    @staticmethod
    def find_one(query):
        return Database().DATABASE[Database.user_collection].find_one(query)

    @staticmethod
    def encrypt_data(collection):
        encryptedCollection = ""
        return encryptedCollection

    @staticmethod
    def check_username_exists(username):
        query = {
            "username":username
        }
        name_query = Database().DATABASE[Database.user_collection].find_one(query)
        #Check to see if a query was returned.
        if name_query is not None:
            return True
        
        return False
    @staticmethod
    def retrieve_hashed_password(username):
        query = {
            "username": username
        }
        name_query = Database().DATABASE[Database.user_collection].find_one(query)
        return name_query['password']