from pymongo import MongoClient
from datetime import datetime

__client = None
__db = None


def initialize(constring: str):
    global __client
    global __db

    __client = MongoClient(constring)

    __client.server_info()
    __db = __client.communityscraper


def __check() -> bool:
    return __client is not None


def new_scrap(scrap: dict):
    scraps_collection = __db.scraps
    scrap_id = scraps_collection.insert_one(scrap).inserted_id
    return scrap_id


def get_scraps(min_date: datetime, max_date: datetime):
    scraps_collection = __db.scraps
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


def get_streamers(limit: int = 0):
    streamers_collection = __db.streamers

    streamers = []

    for streamer in streamers_collection.find().limit(limit):  # A limit of 0 is equivalent to no limit
        streamers.append(streamer["user_login"])

    return streamers


def close():
    if __check():
        __client.close()
