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

        try:
            self.pool = await asyncpg.create_pool(host=self.host, port=self.port,
                                                  database=self.database, user=self.user, password=self.password)
        except Exception as e:
            raise ConnectionError(e)

    async def batch_upload(self, response_list):
        async with self.pool.acquire() as connection:
            try:
                statements = ""
                for coin_id, currency_data in response_list.items():
                    for api_call in currency_data:
                        del api_call['Data'][0]  # Erase first to prevent inserting an existing key, ruining the batch insert
                        for d in api_call['Data']:
                            v = str.format("{},{},{},{},{},{}", d["time"], coin_id, d["open"], d["close"], d["high"], d["low"])
                            statements += '''INSERT INTO ''' + self.history_table + ''' VALUES('''+v+''');'''  # Batch
                await connection.execute(statements)
            except asyncpg.UniqueViolationError:
                pass

    async def get_last_since(self):
        async with self.pool.acquire() as connection:
            last = await connection.fetchval('''SELECT MAX(time) FROM ''' + self.history_table + ''';''')
            if last is None:
                last = Configuration.config["epoch_default"]

        return last
