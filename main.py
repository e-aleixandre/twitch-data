# IMPORTS
from classes import Twitch, Model
import threading
import logging
import dotenv
import os
import sys


# Utility functions
def _handle_streamer(streamer: str) -> None:
    if twitch.is_live(streamer):
        chatters = twitch.get_current_chatters(streamer)
        with data_lock:
            data[streamer] = chatters


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

# STARTING
logging.info("Started scrapping")
logging.info("Trying to get an authorization")
twitch.get_access_token(os.getenv("CLIENTID"), os.getenv("SECRET"))

streamers = Model.get_streamers()

# Generate threads
for streamer in streamers:
    t = threading.Thread(target=_handle_streamer, args=(streamer,))
    t.start()
    threads.append(t)

# Join threads
_join_threads()

print(data)

Model.close()
