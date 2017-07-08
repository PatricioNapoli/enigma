import asyncio
import math
import time
from abc import ABC, abstractmethod

import requests
from config.config import Configuration
from spinner.spinner import Spinner

from database.database import Database


class Gatherer(ABC):
    def __init__(self):
        self.currencies = Configuration.config["currencies"]
        self.currency_conversion = Configuration.config["currency_conversion"]
        self.api_histo_hour_limit = Configuration.config["api_histo_hour_limit"]
        self.api_histo_hour_url = Configuration.config["api_histo_hour_url"]
        self.db_config = Configuration.config["database"]
        self.database = Database(self.db_config["host"],
                                 self.db_config["port"],
                                 self.db_config["database"],
                                 self.db_config["user"],
                                 self.db_config["password"])
        self.loop = asyncio.get_event_loop()

    @abstractmethod
    async def gather(self):
        pass

    def get_info(self):
        return "Gathering for currencies: " + str(self.currencies) + \
               " - Physical currency: " + self.currency_conversion + " - "

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
        self.hours_needed = math.ceil((time.time() - self.since) / 3600)
        self.spinner = Spinner()

    async def gather(self):
        start_time = time.time()

        print(self.get_info() + "Since epoch: " + str(self.since))
        print("Downloading " + str(self.hours_needed) + " hours per currency.")
        print("API hours per call limit: " + str(self.api_histo_hour_limit) +
              " - API calls needed per currency: " + str(math.ceil(self.hours_needed / self.api_histo_hour_limit)))
        print("This may take a while.")

        print("Connecting to database for data enveloping.")
        await self.database.open()

        print('Downloading.. ', end='', flush=True)

        await self.start_parallel_gathering()

        print("Time taken: " + str(time.time() - start_time) + " seconds.")

        if self.rtf:
            print("Switching to realtime gatherer.")
            rg = RealtimeGatherer(self.step)
            rg.gather()

    async def start_parallel_gathering(self):
        for i in range(len(self.currencies)):
            hours_left = self.hours_needed
            last_since = self.since + self.api_histo_hour_limit * 3600
            while hours_left > 0:
                self.spinner.spin()

                if hours_left > self.api_histo_hour_limit:
                    h = self.api_histo_hour_limit
                else:
                    h = hours_left

                r = requests.get(self.api_histo_hour_url + "?fsym=" + self.currencies[i]["coin"] +
                                 "&tsym=" + self.currency_conversion +
                                 "&limit=" + str(h) +
                                 "&aggregate=1&toTs=" + str(last_since))

                await self.upload(r.json(), i + 1)

                hours_left -= self.api_histo_hour_limit
                last_since += h * 3600


class RealtimeGatherer(Gatherer):
    def __init__(self, step):
        Gatherer.__init__(self)
        self.step = step

    def gather(self):
        print(self.get_info() + "With step: " + str(self.step) + " seconds")
