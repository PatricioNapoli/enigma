import requests
import time
import math
import asyncio

from abc import ABC, abstractmethod
from gatherer.database import Database
from gatherer.spinner import Spinner

EPOCH_DEFAULT = 1451692800
SECONDS_DEFAULT = 60
CURRENCIES = ["BTC", "ETH", "LTC"]
PHYSICAL_CURRENCY = "USD"

API_HISTO_HOUR_LIMIT = 2000
API_HISTO_HOUR_URL = 'https://min-api.cryptocompare.com/data/histohour'


class Gatherer(ABC):
    def __init__(self):
        # TODO Fetch from INI file?
        self.database = Database("localhost", "5432", "genesis", "genesis", "")
        self.loop = asyncio.get_event_loop()

    @abstractmethod
    def gather(self):
        pass

    def get_info(self):
        return "Gathering for currencies: " + str(CURRENCIES) + \
               " - Physical currency: " + PHYSICAL_CURRENCY + " - "

    async def upload(self, series, coin_id):
        await self.database.upload(series, coin_id)


class SyncGatherer(Gatherer):
    def __init__(self, rts, step):
        Gatherer.__init__(self)
        self.rts = rts
        self.step = step

    def gather(self):
        print(self.get_info() + "Synchronizing")

        if self.rts:
            print("Switching to realtime gatherer.")
            rg = RealtimeGatherer(self.step)
            rg.gather()


class FullGatherer(Gatherer):
    def __init__(self, since, rtf, step):
        Gatherer.__init__(self)
        self.since = int(since)
        self.rtf = rtf
        self.step = step
        self.spinner = Spinner()

    async def gather(self):
        start_time = time.time()

        print(self.get_info() + "Since epoch: " + str(self.since))
        hours_needed = math.ceil((time.time() - self.since) / 3600)

        print("Downloading " + str(hours_needed) + " hours per currency.")
        print("API hours per call limit: " + str(API_HISTO_HOUR_LIMIT) +
              " - API calls needed per currency: " + str(math.ceil(hours_needed / API_HISTO_HOUR_LIMIT)))
        print("This may take a while.")
        print('Downloading.. ', end='', flush=True)

        await self.database.open()

        for i in range(len(CURRENCIES)):
            hours = hours_needed
            last_since = self.since + API_HISTO_HOUR_LIMIT * 3600
            while hours > 0:
                self.spinner.spin()

                if hours > API_HISTO_HOUR_LIMIT:
                    h = API_HISTO_HOUR_LIMIT
                else:
                    h = hours

                print(API_HISTO_HOUR_URL + "?fsym=" + CURRENCIES[i] +
                                 "&tsym=" + PHYSICAL_CURRENCY + "&limit=" + str(h) + "&aggregate=1&toTs=" + str(last_since))
                r = requests.get(API_HISTO_HOUR_URL + "?fsym=" + CURRENCIES[i] +
                                 "&tsym=" + PHYSICAL_CURRENCY + "&limit=" + str(h) + "&aggregate=1&toTs=" + str(last_since))

                await self.upload(r.json(), i + 1)

                hours -= API_HISTO_HOUR_LIMIT
                last_since += h * 3600

        print("Time taken: " + str(time.time() - start_time) + " seconds.")

        if self.rtf:
            print("Switching to realtime gatherer.")
            rg = RealtimeGatherer(self.step)
            rg.gather()


class RealtimeGatherer(Gatherer):
    def __init__(self, step):
        Gatherer.__init__(self)
        self.step = step

    def gather(self):
        print(self.get_info() + "With step: " + str(self.step) + " seconds")
