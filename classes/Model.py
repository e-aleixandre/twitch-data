from pymongo import MongoClient

from datetime import datetime

__client = None
__db = None


def initialize(constring: str):
    global __client
    global __db

    __client = MongoClient(constring)
    try:
        __client.server_info()
        __db = __client.communityscrapper
    except:
        raise RuntimeError


def __check() -> bool:
    return __client is not None


def new_scrap(scrap: dict):
    scraps_collection = __db.scraps
    scrap_id = scraps_collection.insert_one(scrap).inserted_id
    return scrap_id


def get_streamers(limit: int = 0):
    streamers_collection = __db.streamers

    streamers = []

    for streamer in streamers_collection.find().limit(limit):  # A limit of 0 is equivalent to no limit
        streamers.append(streamer["user_login"])

    return streamers


def close():
    if __check():
        __client.close()
