import asyncio
import concurrent.futures
import math
import time
from enum import Enum

import requests

from config.config import Configuration
from spinner.spinner import Spinner
from database.database import Database


class Gatherer(object):
    def __init__(self, args):
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
        self.spinner = Spinner()
        self.args = args
        self.since = 0
        self.step = 0
        self.hours_needed = 0
        self.start_time = time.time()

    def get_info(self):
        return "Gathering for currencies: " + str(self.currencies) + \
               " - Physical currency: " + self.currency_conversion + " - "

    async def gather(self):
        await self.database.open()

        if self.args.s:
            print("Gathering last database epoch for synchronizing...")
            self.since = await self.database.get_last_since()
            await self.full()
        elif self.args.f is not None:
            self.since = int(self.args.f)
            await self.full()

        if self.args.rt is not None:
            print("Switching to realtime gatherer.")
            self.step = self.args.rt
            self.realtime()

    async def full(self):
        self.hours_needed = math.ceil(((time.time() - 3600) - self.since) / 3600)

        if self.hours_needed == 1:
            print("Database up to date!")
            return

        print(self.get_info() + "Since epoch: " + str(self.since))
        print("Downloading " + str(self.hours_needed) + " hours per currency.")
        print("API hours per call limit: " + str(self.api_histo_hour_limit) +
              " - API calls needed per currency: " + str(math.ceil(self.hours_needed / self.api_histo_hour_limit)))

        print('Downloading.. ', end='', flush=True)

        await self.start_parallel_gathering()

        print("Time taken: " + str(time.time() - self.start_time) + " seconds.")

    async def start_parallel_gathering(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            loop = asyncio.get_event_loop()
            futures = [
                loop.run_in_executor(
                    executor,
                    self.get_currency_data_worker,
                    i
                )
                for i in range(len(self.currencies))
            ]
            for response in await asyncio.gather(*futures):
                pass

    def get_currency_data_worker(self, i):
        hours_left = self.hours_needed
        last_since = self.since + self.api_histo_hour_limit * 3600
        while hours_left > 0:
            self.spinner.spin()

            if hours_left > self.api_histo_hour_limit:
                h = self.api_histo_hour_limit
            else:
                h = hours_left

            print(self.api_histo_hour_url + "?fsym=" + self.currencies[i]["coin"] +
                             "&tsym=" + self.currency_conversion +
                             "&limit=" + str(h) +
                             "&aggregate=1&toTs=" + str(last_since))
            r = requests.get(self.api_histo_hour_url + "?fsym=" + self.currencies[i]["coin"] +
                             "&tsym=" + self.currency_conversion +
                             "&limit=" + str(h) +
                             "&aggregate=1&toTs=" + str(last_since))

            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                loop = asyncio.new_event_loop()  # Create event loop, we are outside main loop.
                loop.run_in_executor(
                    executor,
                    self.database.upload,
                    r.json(),
                    self.currencies[i]["id"]
                )

            #loop = asyncio.new_event_loop()
            #loop.run_until_complete(self.database.upload(r.json(), self.currencies[i]["id"]))

            hours_left -= self.api_histo_hour_limit
            last_since += h * 3600

    def realtime(self):
        print(self.get_info() + "With step: " + str(self.step) + " seconds")
