import requests
import operator


class CoinDeskAPI:
    def __init__(self, currencies=None):
        self.currencies = currencies or ['USD', 'CNY']
        supporeted_currencies = list(
            map(operator.itemgetter('currency'), self._supporeted_currencies())
        )
        assert all(c in supporeted_currencies for c in self.currencies)

    def _supporeted_currencies(self):
        return requests.get(
            'http://api.coindesk.com/v1/bpi/supported-currencies.json').json()

    def _price(self, currency):
        return requests.get(
            f'http://api.coindesk.com/v1/bpi/currentprice/{currency}.json'
        ).json()['bpi'][currency]['rate_float']

    def _time(self):
        return requests.get(
            f'http://api.coindesk.com/v1/bpi/currentprice.json'
        ).json()['time']['updated']

    def prices(self):
        return {
            currency: self._price(currency) for currency in self.currencies
        }, self._time()


if __name__ == '__main__':
    api = CoinDeskAPI()
    print(api.prices())
