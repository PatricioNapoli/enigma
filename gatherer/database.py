import asyncpg


HISTORY_TABLE = "coins_history"


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

    async def upload(self, series, coin_id):
        for d in series['Data']:
            try:
                await self.insert.fetchval(d["time"], coin_id, d["open"], d["close"], d["high"], d["low"])
            except asyncpg.UniqueViolationError:
                pass

    async def close(self):
        await self.connection.close()