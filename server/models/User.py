class User:
    def __init__(self, username, password, balance=100000, assets={}, trades=[]):
        self.username = username
        self.password = password
        self.balance = balance
        self.assets = assets
        self.trades = trades
    
    def return_query_data(self):
        query = {
            "username": self.username,
            "password": self.password,
            "balance": self.balance,
            "assets": self.assets,
            "trades": self.trades,
        }

        return query