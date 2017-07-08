import asyncio
import asyncpg

from config.config import Configuration


class Database(object):
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.history_table = Configuration.config["database"]["history_table"]

    async def open(self):
        print("Connecting to database for data enveloping.")
        self.pool = await asyncpg.create_pool(host=self.host, port=self.port,
                                              database=self.database, user=self.user, password=self.password,
                                              min_size=50, max_size=500)

    def upload(self, series, coin_id):
        loop = asyncio.new_event_loop()
        connection = loop.run_until_complete(self.pool.acquire())
        try:
            print(series)
            statements = ""
            del series['Data'][0]  # Erase first to prevent inserting an existing key, ruining the batch insert
            for d in series['Data']:
                v = str.format("{},{},{},{},{},{}", d["time"], coin_id, d["open"], d["close"], d["high"], d["low"])
                statements += '''INSERT INTO ''' + self.history_table + ''' VALUES('''+v+''');'''  # Batch
            loop.run_until_complete(connection.execute(statements)) # This only blocks this method, don't worry.
        finally:
            loop.run_until_complete(self.pool.release(connection))

    async def get_last_since(self):
        async with self.pool.acquire() as connection:
            last = await connection.fetchval('''SELECT MAX(time) FROM ''' + self.history_table + ''';''')
            if last is None:
                last = Configuration.config["epoch_default"]
            return last
