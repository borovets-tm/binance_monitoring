import asyncio
import configparser
import json
import os
from time import sleep

from binance import AsyncClient

settings = os.path.join('', 'settings.ini')
config = configparser.ConfigParser()
config.read(settings)
api_key = config['SYSTEM']['API_KEY']
api_secret = config['SYSTEM']['API_SECRET']


async def main():
    client = await AsyncClient.create(api_key, api_secret)

    tickers = await client.get_ticker()
    data_list = json.loads(json.dumps(tickers))
    for data in data_list:
        symbol = data.get('symbol')
        max_price = float(data.get('highPrice'))
        current_price = float(data.get('lastPrice'))
        if max_price > current_price and current_price / max_price < 0.991:
            print('The current price %(symbol)s has decreased by approximately %(percent)s percents from the maximum'
                  % {
                        'symbol': symbol,
                        'percent': round((1 - current_price / max_price) * 100, 2)
                    }
                  )

    await client.close_connection()

if __name__ == "__main__":

    while True:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        sleep(59)
