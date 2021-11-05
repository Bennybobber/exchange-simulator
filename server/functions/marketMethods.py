import requests
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

def getTradablePairs():
    binancePairs = getBinancePairs()
    coinGeckoPairs = getCoinGeckoCoins()
    return filterPairs(coinGeckoPairs, binancePairs)

def getBinancePairs():  
    pairs = []
    try:
        url = 'https://api.binance.com/api/v1/exchangeInfo'
        response = requests.get(url)
        symbols = response.json()['symbols']
        for symbol in symbols:
            if (symbol['symbol'][-4:] == 'USDT'):
                pairs.append(symbol)
        return pairs 
    except Exception as err:
        return err

def getCoinGeckoCoins():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
        response = requests.get(url)
        pairs = response.json()
        # pp.pprint(pairs)
        return pairs
    except Exception as err:
        return err

def sort_by_marketcap(e):
    return e['market_cap_rank']

def filterPairs(coinGeckoPairs, binancePairs):
    filteredPairs = []
    for item in coinGeckoPairs:
        if (item['symbol'].upper() == 'USDT' ):
            filteredPairs.append(item)
            continue   
        for coin in binancePairs:
            if(item['symbol'].upper() == coin['symbol'][:-4]):
                filteredPairs.append(item)
                break
    filteredPairs.sort(key=sort_by_marketcap)
    print(len(filteredPairs))
    return filteredPairs

