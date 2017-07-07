from abc import ABC, abstractmethod
import requests
import time
import math

EPOCH_DEFAULT = 1451692800
SECONDS_DEFAULT = 60
CURRENCIES = ["BTC", "ETH", "LTC"]
PHYSICAL_CURRENCY = "USD"

API_HISTO_HOUR_LIMIT = 2000
API_HISTO_HOUR_URL = 'https://min-api.cryptocompare.com/data/histohour'


def get_info():
    return "Gathering for currencies: " + str(CURRENCIES) + \
           " - Physical currency: " + PHYSICAL_CURRENCY + " - "


class Gatherer(ABC):
    @abstractmethod
    def gather(self):
        pass


class SyncGatherer(Gatherer):
    def __init__(self, rts, step):
        self.rts = rts
        self.step = step

    def gather(self):
        print(get_info() + "Synchronizing")

        if self.rts:
            print("Switching to realtime gatherer.")
            rg = RealtimeGatherer(self.step)
            rg.gather()


class FullGatherer(Gatherer):
    def __init__(self, since, rtf, step):
        self.since = since
        self.rtf = rtf
        self.step = step

    def gather(self):
        print(get_info() + "Since epoch: " + str(self.since))
        hours_needed = math.ceil((time.time() - int(self.since)) / 3600)
        print("Downloading " + str(hours_needed) + " hours.")
        print("This may take a while.")

        for i in range(len(CURRENCIES)):
            hours = hours_needed
            while hours > 0:
                if hours > API_HISTO_HOUR_LIMIT:
                    h = API_HISTO_HOUR_LIMIT
                else:
                    h = hours

                r = requests.get(API_HISTO_HOUR_URL + "?fsym=" + CURRENCIES[i] +
                                 "&tsym=" + PHYSICAL_CURRENCY + "&limit=" + str(h) + "&aggregate=1&toTs=" + str(self.since))
                print(r.json())
                hours -= API_HISTO_HOUR_LIMIT

        if self.rtf:
            print("Switching to realtime gatherer.")
            rg = RealtimeGatherer(self.step)
            rg.gather()


class RealtimeGatherer(Gatherer):
    def __init__(self, step):
        self.step = step

    def gather(self):
        print(get_info() + "With step: " + str(self.step) + " seconds")
