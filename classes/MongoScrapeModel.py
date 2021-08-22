from pymongo import MongoClient
from datetime import datetime
from .interfaces.ScrapeModelInterface import ScrapeModelInterface


class MongoScrapeModel(ScrapeModelInterface):

    def __init__(self, constring: str, database: str):
        self.__client = MongoClient(constring)
        self.__client.server_info()
        self.__db = self.__client[database]

    def _check(self) -> bool:
        return self.__client is not None

    def new_scrape(self, scrape: dict):
        scrapes_collection = self.__db.scrapes
        scrape_id = scrapes_collection.insert_one(scrape).inserted_id
        return scrape_id

    def get_scrapes(self, min_date: datetime, max_date: datetime):
        scrapes_collection = self.__db.scrapes
        params = {
            "created_at": {
                "$gte": min_date,
                "$lte": max_date
            }
        }

        scrapes = []

        for scrape in scrapes_collection.find(params):
            scrapes.append(scrape)

        return scrapes

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
