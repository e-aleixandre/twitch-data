from pymongo import MongoClient
import boto3
from boto3.dynamodb.conditions import Key
import uuid
from datetime import datetime

__client: any = None
__db = None
__mongo = True


def initialize(constring: str):
    global __client
    global __mongo

    if constring == "dynamo":
        __mongo = False
        __client = boto3.resource("dynamodb")
    else:
        __initialize_mongo(constring)


def __check() -> bool:
    return __client is not None


def __initialize_mongo(constring: str):
    global __client
    global __db

    __client = MongoClient(constring)

    __client.server_info()
    __db = __client.communityscrapper


def __generate_dynamo_id() -> str:
    if __mongo:
        raise RuntimeError("Attempted to execute a dynamodb related function when dbms is not dynamodb")

    table = __client.Table('scraps')
    while True:
        id = uuid.uuid4().hex
        response = table.query(KeyConditionExpression=Key('_id').eq(id))
        if response["Count"] == 0:
            break

    return id


def new_scrap(scrap: dict):
    now = datetime.utcnow()

    if __mongo:
        scraps_collection = __db.scraps
        scrap["created_at"] = now
        scrap_id = scraps_collection.insert_one(scrap).inserted_id
    else:
        scraps_collection = __client.Table('scraps')
        scrap_id = __generate_dynamo_id()
        scrap["_id"] = scrap_id
        scrap["created_at"] = now.strftime("%Y-%m-%dT%H:%M")
        scraps_collection.put_item(Item=scrap)

    return scrap_id


def get_scraps(min_date: datetime, max_date: datetime):
    if __mongo:
        scraps_collection = __db.scraps
        params = {
            "created_at": {
                "$gte": min_date,
                "$lte": max_date
            }
        }
        response = scraps_collection.find(params)
    else:
        min_date = min_date.strftime("%Y-%m-%dT%H:%M")
        max_date = max_date.strftime("%Y-%m-%dT%H:%M")
        table = __db.Table('scraps')
        response = table.query(
            KeyConditionExpression=Key('created_at').gte(min_date) & Key('created_at').lte(max_date)
        )
        response = response['Items']

    scraps = []

    for scrap in response:
        scraps.append(scrap)

    return scraps


def get_streamers(limit: int = 0):
    if __mongo:
        streamers_collection = __db.streamers
        response = streamers_collection.find().limit(limit)
    else:
        table = __client.Table('streamers')

        response = []
        args = {
            "Limit": limit
        }
        done = False
        start_key = None
        while not done:
            if start_key:
                args["ExclusiveStartKey"] = start_key
            scan_result = table.scan(**args)
            response.extend(scan_result["Items"])
            start_key = scan_result.get("LastEvaluatedKey", None)
            done = start_key is None

    streamers = []

    for streamer in response:  # A limit of 0 is equivalent to no limit
        streamers.append(streamer["user_login"])

    return streamers


def close():
    if __check() and __mongo:
        __client.close()
