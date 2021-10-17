# import urllib library
from urllib.request import urlopen, Request
  
# import json
import json

def main():
    # store the URL in url as 
    # parameter for urlopen
    url = "https://api.babylons.io/v1/collections/collectibles?$skip=0&$take=48&$sortField=orderBuyPrice&$sortOrder=asc&$filters=Birth:$:between:$:,&$filters=IncreaseMutantRate:$:between:$:,&$filters=TimeReduce:$:between:$:,&tokenAddress=0x12f299cb26452b428017340e79f79662ac8d73ef&onSale=true&lang=en"
    url2 = "https://api.babylons.io/v1/collections/collectibles?$skip=0&$take=48&$sortField=orderBuyPrice&$sortOrder=asc&$filters=$$currency:$:in:$:WANA&$filters=Birth:$:between:$:,&$filters=IncreaseMutantRate:$:between:$:,&$filters=TimeReduce:$:between:$:,&tokenAddress=0x12f299cb26452b428017340e79f79662ac8d73ef&onSale=true&lang=en"
    
    # store the response of URL
    r = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    r2 = Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(r).read()
    response2 = urlopen(r2).read()

    
    # storing the JSON response 
    # from url in data
    data_json = json.loads(response)
    data_json2 = json.loads(response2)

    # get the prices
    bnb_price = data_json['data']['rows'][0]['orderBuyPrice']
    wana_price = data_json2['data']['rows'][0]['orderBuyPrice']
    return bnb_price, wana_price