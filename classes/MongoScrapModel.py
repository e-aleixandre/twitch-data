from pymongo import MongoClient
from datetime import datetime
from .interfaces.ScrapModelInterface import ScrapModelInterface


class MongoScrapModel(ScrapModelInterface):

    def __init__(self, constring: str, database: str):
        self.__client = MongoClient(constring)
        self.__client.server_info()
        self.__db = self.__client[database]

    def _check(self) -> bool:
        return self.__client is not None

    def new_scrap(self, scrap: dict):
        scraps_collection = self.__db.scraps
        scrap_id = scraps_collection.insert_one(scrap).inserted_id
        return scrap_id

    def get_scraps(self, min_date: datetime, max_date: datetime):
        scraps_collection = self.__db.scraps
        params = {
            "created_at": {
                "$gte": min_date,
                "$lte": max_date
            }
        }

        scraps = []

        for scrap in scraps_collection.find(params):
            scraps.append(scrap)

        return scraps

    def get_streamers(self, limit: int = 0):
        streamers_collection = self.__db.streamers

        streamers = []

        for streamer in streamers_collection.find().limit(limit):  # A limit of 0 is equivalent to no limit
            streamers.append(streamer["user_login"])

        return streamers

    def indexes(self, collection: str):
        return self.__db[collection].index_information()

    def close(self):
        if self._check():
            self.__client.close()
