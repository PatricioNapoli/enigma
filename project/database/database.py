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

    async def open(self):
        self.pool = await asyncpg.create_pool(host=self.host, port=self.port,
                                              database=self.database, user=self.user, password=self.password)

    def upload(self, series, coin_id):
        with self.pool.acquire() as connection:
            statements = ""
            del series['Data'][0]  # Erase first to prevent inserting an existing key, ruining the batch insert
            for d in series['Data']:
                v = str.format("{},{},{},{},{},{}", d["time"], coin_id, d["open"], d["close"], d["high"], d["low"])
                statements += '''INSERT INTO ''' + Configuration.config["database"]["history_table"] + ''' VALUES('''+v+''');'''
            try:
                asyncio.get_event_loop().run_until_complete(connection.execute(statements))  # This is non-blocking, don't worry.
            except asyncpg.UniqueViolationError as e:
                print(e.args)
                pass
