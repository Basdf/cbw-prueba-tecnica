from pymongo import AsyncMongoClient

from app.configs.settings import settings


class MongoDBConfig:
    def __init__(self, uri: str, db_name: str):
        self.client = AsyncMongoClient(uri)
        self.db = self.client.get_database(db_name)

    def get_collection(self, collection_name: str):
        return self.db.get_collection(collection_name)

    def close_connection(self):
        self.client.close()


mongo_db = MongoDBConfig(uri=settings.MONGO_URI, db_name=settings.MONGO_DB_NAME)
