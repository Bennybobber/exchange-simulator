class User:
    def __init__(self, username, password, balance=100000, assets={}):
        self.username = username
        self.password = password
        self.balance = balance
        self.assets = assets
    
    def return_query_data(self):
        query = {
            "username": self.username,
            "password": self.password,
            "balance": self.balance,
            "assets": self.assets
        }

        return query