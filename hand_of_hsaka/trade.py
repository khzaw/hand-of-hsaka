from dotenv import dotenv_values
from binance.exceptions import BinanceAPIException
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager, AsyncClient, BinanceSocketManager
import asyncio
import json

config = {
  **dotenv_values("../.env")
}

class ArbClient:
    @classmethod
    async def create(cls, api, secret, test=True):
        self = ArbClient()
        self.client = await AsyncClient.create(
          api,
          secret,
          testnet=test
        )
        return self

    def _get_avg_fill(self, fills, quantity):
        return sum([float(f['price']) * (float(f['qty']) / quantity) for f in fills])

    async def buy(self, symbol, quantity):
        try:
          market_res = await self.client.order_market_sell(symbol=symbol, quantity=quantity)
        except BinanceAPIException as e:
            print(e)
        else:
            # print(json.dumps(market_res, indent=2))
            fill = self._get_avg_fill(market_res['fills'], quantity)
            print(fill)
        await self.client.close_connection()


async def main():
    arb = await ArbClient.create(
      config['BINANCE_TESTNET_API'],
      config['BINANCE_TESTNET_SECRET'])

    await arb.buy('BTCUSDT', 0.001)


if __name__ == "__main__":
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  loop.run_until_complete(main())
  loop.close()
