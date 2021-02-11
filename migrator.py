import pymongo
import boto3
from boto3.dynamodb.conditions import Key
from classes import Twitch, Model
import uuid
import os
from datetime import datetime, timedelta

mongo = pymongo.MongoClient("mongodb://communityscrapper:%5E9ziv4WW!Iy!5%24HO@35.180.27.94")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('scraps')

scraps = mongo.communityscrapper.scraps

for scrap in scraps.find():
    # Getting the object ready
    obj = {
        "_id": None,
        "streamers": scrap["streamers"],
        "created_at": scrap["created_at"].strftime("%Y-%m-%dT%H:%M")
    }
    # Ensuring a unique id
    while True:
        id = uuid.uuid4().hex
        response = table.query(KeyConditionExpression=Key('_id').eq(id))
        if response["Count"] == 0:
            break

    obj["_id"] = id

    response = table.put_item(Item=obj)
    if response["ResponseMetaData"]["HTTPStatusCode"] != 200:
        print("Error on: ", scrap["_id"])

"""
streamers = Model.get_streamers()

print(streamers)

table = dynamodb.Table('streamers')
for streamer in streamers:
    obj = {
        "user_login": streamer
    }
    table.put_item(Item=obj)
"""

"""
table = dynamodb.create_table(
    TableName='scraps',
    KeySchema=[
        {
            'AttributeName': '_id',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'created_at',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': '_id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'created_at',
            'AttributeType': 'S'
        }

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

"""
"""
Scraps: 
{
    "_id": aijsdasj9a83jd9a83da3d,
    "streamers": [
        "lavisanteta": ["viewer1", "viewer2", "viewer3"],
        "another1": ["viewer4", "viewer5"]
    ],
    "created_at": datetime
}
Streamers:
{
    "_id": asidjaoisjdaiosdjad,
    "user_login": "lavisanteta"
}
"""

