from pymongo import AsyncMongoClient


class MongoDBConfig:
    def __init__(self, uri: str, db_name: str):
        self.client = AsyncMongoClient(uri)
        self.db = self.client.get_database(db_name)

    def get_collection(self, collection_name: str):
        return self.db.get_collection(collection_name)

    async def close_connection(self):
        await self.client.close()
