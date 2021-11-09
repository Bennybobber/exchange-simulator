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
    headers= {
        "Authorization": "Bearer 57401018-8c1c-4d0c-8c51-7116a7cba133"
    }
    try:
        url = 'https://api.coincap.io/v2/assets'
        response = requests.get(url, headers)
        print(response.status_code)
        if (response.status_code == 429):
            return
        coins = response.json()['data']
        return coins 
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
    try:
        for item in coinGeckoPairs:  
            for coin in binancePairs:
            
                if(item['symbol'].upper() == coin['symbol']):
                    coin['image'] = item['image']
                    coin['high_24h'] = item['high_24h']
                    coin['price_change_percentage_24h'] = item['price_change_percentage_24h']
                    coin['market_cap_rank'] = item['market_cap_rank']
                    coin['market_cap'] = item['market_cap']
                    coin['current_price'] = item['current_price']
                    coin.pop('rank', None)
                    coin.pop('marketCapUsd', None)
                    coin.pop('priceUsd', None)
                    filteredPairs.append(coin)
                    break
        filteredPairs.sort(key=sort_by_marketcap)
        return filteredPairs
    except Exception as err:
        print('error')
        print(err)

def specific_coin(coin):
    url = f"https://api.coincap.io/v2/assets/{coin}"
    response = requests.get(url)
    return response.json()

def get_coin_history(coin, interval):
    try:
        headers= {
        "Authorization": "Bearer 57401018-8c1c-4d0c-8c51-7116a7cba133"
        }
        url = f"https://api.coincap.io/v2/candles?exchange=binance&interval={interval}&baseId={coin}&quoteId=tether"
        response = requests.get(url, headers)
        print('PRINTING RESPONSE....')
        print(response.status_code)
        if (response.status_code == 429):
            return response
        return response.json()
    except Exception as err:
        print(err)
        return err
