from abc import ABC, abstractmethod
import requests
import time
import math
import itertools
import sys
import asyncio
import asyncpg

EPOCH_DEFAULT = 1451692800
SECONDS_DEFAULT = 60
CURRENCIES = ["BTC", "ETH", "LTC"]
PHYSICAL_CURRENCY = "USD"

HISTORY_TABLE = "coins_history"

API_HISTO_HOUR_LIMIT = 2000
API_HISTO_HOUR_URL = 'https://min-api.cryptocompare.com/data/histohour'


class Database(object):
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    async def open(self):
        self.connection = await asyncpg.connect(host=self.host, port=self.port,
                                                database=self.database, user=self.user, password=self.password)
        self.insert = await self.connection.prepare('''INSERT INTO ''' + HISTORY_TABLE + ''' VALUES($1, $2, $3, $4, $5, $6)''')

    async def upload(self, d, coin_id):
        await self.insert.fetchval(d["time"], coin_id, d["open"], d["close"], d["high"], d["low"])

    async def close(self):
        await self.connection.close()


class Gatherer(ABC):
    def __init__(self):
        # TODO Fetch from INI file?
        self.database = Database("localhost", "5432", "genesis", "genesis", "")
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.database.open())

    @abstractmethod
    def gather(self):
        pass

    def get_info(self):
        return "Gathering for currencies: " + str(CURRENCIES) + \
               " - Physical currency: " + PHYSICAL_CURRENCY + " - "

    def upload(self, series, coin_id):
        for d in series['Data']:
            self.loop.run_until_complete(self.database.upload(d, coin_id))


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
        self.since = since
        self.rtf = rtf
        self.step = step

    def gather(self):
        print(self.get_info() + "Since epoch: " + str(self.since))
        hours_needed = math.ceil((time.time() - int(self.since)) / 3600)
        print("Downloading " + str(hours_needed) + " hours.")
        print("This may take a while.")
        print('Downloading.. ', end='', flush=True)

        spinner = Spinner()

        for i in range(len(CURRENCIES)):
            hours = hours_needed
            while hours > 0:
                spinner.spin()

                if hours > API_HISTO_HOUR_LIMIT:
                    h = API_HISTO_HOUR_LIMIT
                else:
                    h = hours

                r = requests.get(API_HISTO_HOUR_URL + "?fsym=" + CURRENCIES[i] +
                                 "&tsym=" + PHYSICAL_CURRENCY + "&limit=" + str(h) + "&aggregate=1&toTs=" + str(self.since))

                self.upload(r.json(), i+1)

                hours -= API_HISTO_HOUR_LIMIT

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


class Spinner(object):
    def __init__(self):
        self.spinner = itertools.cycle(['-', '\\', '|', '/'])

    def spin(self):
        sys.stdout.write(self.spinner.__next__())
        sys.stdout.flush()
        sys.stdout.write('\b')
