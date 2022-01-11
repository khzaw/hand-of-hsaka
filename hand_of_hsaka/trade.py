from dotenv import dotenv_values
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager, AsyncClient, BinanceSocketManager
import asyncio

config = {
  **dotenv_values("../env")
}

# the async keyword in front of the function defines it as a couroutine.
# If you call a coroutine directly the function isn't executed, you just get the coroutine back.
# To actually execute the coroutine we use the await keyword.

class BinanceClient:
    def __init__(self):
        pass

async def order_book(client, symbol):
    order_book = await client.get_order_book(symbol=symbol)
    print(order_book)


async def kline_listener(client):
  bm = BinanceSocketManager(client)
  symbol = 'BNBBTC'
  res_count = 0
  async with bm.kline_socket(symbol=symbol) as stream:
    while True:
      res = await stream.recv()
      res_count += 1
      print(res)
      if res_count == 5:
          res_count = 0
          loop.call_soon(asyncio.create_task, order_book(client, symbol))


async def main():
  client = await AsyncClient.create(config['BINANCE_API'], config['BINANCE_SECRET'], testnet=True)
  await kline_listener(client)


# asyncio runs with an event loop,
if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())


client = Client(config['BINANCE_API'], config['BINANCE_SECRET'])

# get market depth
depth = client.get_order_book(symbol='BNBBTC')
