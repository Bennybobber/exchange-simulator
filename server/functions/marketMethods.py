
def topTen(marketData):
    topTen = {}
    for x in marketData:
        topTen[x] = marketData[x]
        print("X IS: " + x)
        if x is 11:
            break
            
    return topTen