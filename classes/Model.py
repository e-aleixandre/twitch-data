import psycopg2
import datetime

__connector = None
__cursor = None

def initialize(constring: str):
    global __connector
    __connector = psycopg2.connect(constring)

def close():
    if __connector is not None:
        __connector.close()

def get_scraps(start_date: datetime, end_time: datetime):
    pass

def get_streamers():
    pass