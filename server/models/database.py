import pymongo
import bcrypt
class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None
    user_collection = 'user_accounts'

    @staticmethod
    def initialize(URI):
        """
        initializes the database with the SimEx database
        :params:
            URI (String): string to the address of the local database

        :return:

        """
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['SimEx']
    

    @staticmethod
    async def insert_new_user(data):
        """
        Inserts a new user into the SimEx collection
        :params:
            data (dict): dictionary containing all user data
        :return:

        """
        Database.DATABASE[Database.user_collection].insert(data)
    @staticmethod
    async def delete_user(data):
        """
        Deletes a user from the database
        :params:
            data (string): string containing the username to be made into
            a query, so that deletion can take place.
        :return:

        """
        query = {
            "username": data
        }
        Database.DATABASE[Database.user_collection].delete_one(query)

    @staticmethod
    async def update_user(data):
        """
        Updates a new user record in the SimEx collection
        :params:
            data (dict): dictionary containing the new updated user data
        :return:

        """
        data['password'] = await Database.retrieve_hashed_password(data['username'])
        query = {
            "username": data['username']
        }
        currentUser = await Database().find_one(query)
        Database.DATABASE[Database.user_collection].replace_one(query, data)

    @staticmethod
    async def find():
        """
        returns tne entire SimEx collection
        :params:
        :return:

        """
        return Database().DATABASE[Database.user_collection].find()

    @staticmethod
    async def find_one(query):
        """
        Finds a user record in the dictionary
        :params:
            query (dict): dictionary containing the query data 
        :return:
            user (dict): returns one user object dictionary
        """
        user = Database().DATABASE[Database.user_collection].find_one(query)
        return user

    @staticmethod
    async def check_username_exists(username):
        """
        Checks for a given username in the SimEx collection
        :params:
            username (String): A String variable username is passed in 
        :return:
            (bool): True if name found, False if name not found
        """
        query = {
            "username":username
        }
        name_query = await Database().find_one(query)
        #Check to see if a query was returned.
        if name_query is not None:
            return True
        
        return False
    @staticmethod
    async def retrieve_hashed_password(username):
        """
        Retireves the hashed password to check against the incoming password
        in a loginr request
        :params:
            username (String): The username of the user we want to check the password
            for
        :return:
            name_query['password'] (String): The hashed password from the
            database to check.
        """
        query = {
            "username": username
        }
        name_query = await Database().find_one(query)
        return name_query['password']

    @staticmethod
    async def retrieve_user_portfolio(username):
        """
        Retrieves a users portfolio, making sure to remove the password and id from the 
        returned data first.
        :params:
            username (String): The username of the user we want to retrieve the portfolio of
        :return:
            user_portfolio (dict): User dictionary which contains all their portfolio data.
        """
        query = {
            "username": username
        }
        user_portfolio = Database().DATABASE[Database.user_collection].find_one(query, {'password': 0, '_id':0})
        return user_portfolio