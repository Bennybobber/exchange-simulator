import requests
import json
import asyncio
import time

async def getTradablePairs():
    """
    Retrieves all tradable pairs

    :params: 0

    :return:
        filteredPairs (dict): dictionary of all filtered pairs

    """
    coinapiPairs = await getCoinapiPairs()
    coinGeckoPairs = await getCoinGeckoCoins()
    return await filterPairs(coinGeckoPairs, coinapiPairs)

async def getCoinapiPairs(): 
    """
    Retrieves the CoinAPI pairs

    :params:
    :return:
        pairs: (dict) Dictionary of coinAPI crypto pairs

    """
    pairs = []
    headers= {
        "Authorization": "Bearer 57401018-8c1c-4d0c-8c51-7116a7cba133"
    }
    try:
        # Keep trying to get the data but don't spam (wait 5 seconds)
        while True:
            url = 'https://api.coincap.io/v2/assets'
            response = requests.get(url, headers)
            if (response.status_code == 200):
                break
            else:
                time.sleep(5)
        if (response.status_code == 429):
           raise Exception('Public API Failure')
        pairs = response.json()['data']
        return pairs 
    except Exception as err:
        return err

async def getCoinGeckoCoins():
    """
    Retrieves the coinGecko API pairs

    :params:
    :return:
        pairs (dict): Dictionary of coinGecko API crypto pairs 

    """
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
        response = requests.get(url)
        pairs = response.json()
        return pairs
    except Exception as err:
        return err

def sort_by_marketcap(e):
    """
    Sets the sort to marketcap

    :params:
        e: dictionary parameter to sort by

    :return: 
        e (String): filter set to market_cap_rank

    """
    return e['market_cap_rank']

async def filterPairs(coinGeckoPairs, coinapiPairs):
    """
    Filters between the two dictionary of pairs

    :params:
        coinGeckoPairs (dict): A dictionary of coinGeckoPairs
        coinapiPairs (dict): A dictionary of coinapiPairs

    :return:
        filteredPairs (dict): Dictionary of filtered apirs

    """
    filteredPairs = []
    try:
        for item in coinGeckoPairs:  
            for coin in coinapiPairs:
                if(item['symbol'].upper() == coin['symbol']):
                    item['id'] = coin['id']
                    filteredPairs.append(item)
                    break
        filteredPairs.sort(key = sort_by_marketcap)
        return filteredPairs
    except Exception as err:
        print('error')
        print(err)

async def specific_coin(symbol):
    """
    Filters between the two dictionary of pairs

    :params:
        symbol (String): the asset symbol used to identify the pair

    :return:
        coin (dict): Dictionary of data for a specific coin

    """
    coingecko = await getCoinGeckoCoins()
    for coin in coingecko:
        if coin['symbol'] == symbol.lower():
            return coin
    return False
   
    

async def get_coin_history(coin, interval):
    """
    Filters between the two dictionary of pairs

    :params:
    :return:
        history (dict): Dictionary of candelstick history data

    """
    try:
        headers= {
        "Authorization": "Bearer 57401018-8c1c-4d0c-8c51-7116a7cba133"
        }
        url = f"https://api.coincap.io/v2/candles?exchange=binance&interval={interval}&baseId={coin}&quoteId=tether"
        history = requests.get(url, headers)
        if (history.status_code == 429):
            return history
        # Try another exchange if binance doesn't support the token.
        if (len(history.json()['data']) == 0):
            url = f"https://api.coincap.io/v2/candles?exchange=okex&interval={interval}&baseId={coin}&quoteId=tether"
            history = requests.get(url, headers)
        if (history.status_code == 429):
            return history
        return history.json()
    except Exception as err:
        print(err)
        return err
