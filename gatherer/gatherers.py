from abc import ABC, abstractmethod
import requests


API_HISTO_HOUR_URL = 'https://min-api.cryptocompare.com/data/histohour'


class Gatherer(ABC):
    def __init__(self, currencies, physical_currency):
        self.currencies = currencies
        self.physical_currency = physical_currency

    @abstractmethod
    def gather(self):
        pass

    def get_info(self):
        return "Gathering for currencies: " + str(self.currencies) + \
               " - Physical currency: " + self.physical_currency + " - "


class FullGatherer(Gatherer):
    def __init__(self, currencies, physical_currency, to):
        Gatherer.__init__(self, currencies, physical_currency)
        self.to = to

    def gather(self):
        print(self.get_info() + "Since epoch: " + str(self.to))
        r = requests.get(API_HISTO_HOUR_URL + "?fsym=" + self.currencies[0] +
                         "&tsym=" + self.physical_currency + "&limit=24&aggregate=1&toTs=" + self.to)
        print(r.json())


class RealtimeGatherer(Gatherer):
    def __init__(self, currencies, physical_currency, step):
        Gatherer.__init__(self, currencies, physical_currency)
        self.step = step

    def gather(self):
        print(self.get_info() + "With step: " + str(self.step) + " seconds")
