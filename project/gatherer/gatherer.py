import asyncio
import concurrent.futures
import math
import time
import requests

from socket import socket, AF_UNIX, SOCK_STREAM

import config
import spinner
import database


class Gatherer(object):
    def __init__(self, args):
        self.currencies = config.Configuration.config["currencies"]
        self.currency_conversion = config.Configuration.config["currency_conversion"]
        self.api_histo_hour_limit = config.Configuration.config["api_histo_hour_limit"]
        self.api_histo_hour_url = config.Configuration.config["api_histo_hour_url"]
        self.db_config = config.Configuration.config["database"]
        self.database = database.Database(self.db_config["host"],
                                 self.db_config["port"],
                                 self.db_config["database"],
                                 self.db_config["user"],
                                 self.db_config["password"])
        self.unix_socket = config.Configuration.config["unix_socket"]
        self.spinner = spinner.Spinner()
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

        if self.hours_needed <= 1:
            print("Database up to date!")
            return

        if self.args.v:
            print(self.get_info() + "Since epoch: " + str(self.since))
            print("Downloading " + str(self.hours_needed) + " hours per currency.")
            print("API hours per call limit: " + str(self.api_histo_hour_limit) +
                  " - API calls needed per currency: " + str(math.ceil(self.hours_needed / self.api_histo_hour_limit)))

        print('Downloading.. ', end='', flush=True)

        if self.args.p:
            await self.start_parallel_gathering()
        else:
            await self.start_gathering()

        print("Time taken: " + str(time.time() - self.start_time) + " seconds.")

    async def start_gathering(self):
        response_list = {}
        url_list = await self.generate_urls()

        for i, u in url_list.items():
            response_list[i] = []

        for coin_id, urls in url_list.items():
            for url in urls:
                self.spinner.spin()
                response_list[coin_id].append((requests.get(url).json()))

        await self.database.batch_upload(response_list)

    async def start_parallel_gathering(self):
        url_list = await self.generate_urls()

        response_list = {}

        total_count = 0
        for i, u in url_list.items():
            response_list[i] = []
            for j in u:
                total_count += 1

        with concurrent.futures.ThreadPoolExecutor(max_workers=total_count) as executor:
            loop = asyncio.get_event_loop()
            futures = [
                loop.run_in_executor(
                    executor,
                    self.get_parallel_response,
                    coin_id,
                    url
                )
                for coin_id, urls in url_list.items()
                    for url in urls
            ]
            for response in await asyncio.gather(*futures):
                self.spinner.spin()
                response_list[response[0]].append(response[1])
                pass

        await self.database.batch_upload(response_list)

    def get_parallel_response(self, coin_id, url):
        return [coin_id, requests.get(url).json()]

    async def generate_urls(self):
        url_list = {}

        for i in range(len(self.currencies)):
            hours_left = self.hours_needed
            last_since = self.since + self.api_histo_hour_limit * 3600

            url_list[self.currencies[i]["id"]] = []

            while hours_left > 0:
                self.spinner.spin()

                if hours_left > self.api_histo_hour_limit:
                    h = self.api_histo_hour_limit
                else:
                    h = hours_left

                if self.args.v:
                    print(self.api_histo_hour_url + "?fsym=" + self.currencies[i]["coin"] +
                          "&tsym=" + self.currency_conversion +
                          "&limit=" + str(h) +
                          "&aggregate=1&toTs=" + str(last_since))

                url_list[self.currencies[i]["id"]].append(self.api_histo_hour_url + "?fsym=" + self.currencies[i]["coin"] +
                                                      "&tsym=" + self.currency_conversion +
                                                      "&limit=" + str(h) +
                                                      "&aggregate=1&toTs=" + str(last_since))

                hours_left -= self.api_histo_hour_limit
                last_since += h * 3600

        return url_list

    def realtime(self):
        if self.args.v:
            print(self.get_info() + "With step: " + str(self.step) + " seconds")

        s = socket(AF_UNIX, SOCK_STREAM)
        s.connect(self.unix_socket)



        s.close()
