import psycopg2
import pytz
from datetime import datetime

__connector = None


def initialize(constring: str):
    global __connector
    __connector = psycopg2.connect(constring)


def __check() -> bool:
    return __connector is not None


def close():
    if __check():
        __connector.close()


def get_scraps(start_time: datetime, end_time: datetime):
    cursor = __connector.cursor()
    query = "SELECT * FROM scraps WHERE created_at BETWEEN %s AND %s"
    cursor.execute(query, (start_time, end_time))

    scraps = cursor.fetchall()
    cursor.close()
    return scraps

def create_scrap():
    cursor = __connector.cursor()
    created_at = datetime.utcnow()
    query = "INSERT INTO scraps (created_at) values (%s)"
    cursor.execute(query, (created_at,))
    __connector.commit()
    cursor.close()


def get_streamers():
    cursor = __connector.cursor()
    query = "SELECT * FROM streamers"
    cursor.execute(query)

    streamers = cursor.fetchall()
    cursor.close()

    return streamers
