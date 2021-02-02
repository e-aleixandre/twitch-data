# IMPORTS
from classes import Twitch, Model
import threading
import logging
import dotenv
from datetime import datetime
import os
import sys


# Utility functions
def _handle_streamer(streamer: str) -> None:
    global data, data_lock

    if twitch.is_live(streamer):
        chatters = twitch.get_current_chatters(streamer)
        with data_lock:
            data[streamer] = chatters
    print("Semaphore released for: ", threading.current_thread().getName())
    semaphore.release()


def _join_threads() -> None:
    for thread in threads:
        thread.join()


# LOADING ENV VARIABLES
dotenv.load_dotenv(".env.local")

# INITIALIZING
logging.basicConfig(filename="twitch-data.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
twitch = Twitch.Twitch()
Model.initialize(os.getenv("DBCON"))
data_lock = threading.Lock()
data = {}
threads = []
semaphore = threading.Semaphore(value=15)

# STARTING
logging.info("Started scrapping")
twitch.get_access_token(os.getenv("CLIENTID"), os.getenv("SECRET"))
streamers = Model.get_streamers()

# Generate threads
for streamer in streamers:
    semaphore.acquire()
    t = threading.Thread(target=_handle_streamer, args=(streamer,))
    print("Semaphore acquired for: ", t.getName())
    t.start()
    threads.append(t)

# Join threads
_join_threads()

logging.info("Finished scrapping")
logging.info("Storing to the DB")
if data:
    try:
        scrap = dict()
        scrap["streamers"] = data
        scrap["created_at"] = datetime.utcnow()
        Model.new_scrap(scrap)
    except:
        logging.error("Data couldn't be saved in the DB, it should be stored in a backup file")
    else:
        logging.info("Data stored correctly")
else:
    logging.info("Data is empty. Nothing to save.")


Model.close()
