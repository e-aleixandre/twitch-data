# IMPORTS
from classes import Twitch, Model
import threading
import logging
import dotenv
from datetime import datetime
from memory_profiler import memory_usage
import os
import pickle


# Utility functions
def _handle_streamer(streamer: str) -> None:
    global data, data_lock

    if twitch.is_live(streamer):
        chatters = twitch.get_current_chatters(streamer)
        with data_lock:
            data[streamer] = chatters

    semaphore.release()


def _join_threads() -> None:
    for thread in threads:
        thread.join()


# Setting CWD because cronjob uses home by default
cwd = os.path.dirname(__file__)
if cwd != '':
    os.chdir(cwd)

# LOADING ENV VARIABLES
dotenv.load_dotenv(".env.local")

# INITIALIZING
logging.basicConfig(filename=os.getenv("LOGS") + "/twitch-data.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
twitch = Twitch.Twitch()

try:
    Model.initialize(os.getenv("DBCON"))
except Exception as e:
    logging.critical("An error occured connecting to the database. Logging the exception.")
    logging.exception(e)
    exit(-1)

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
    t.start()
    threads.append(t)

# Join threads
_join_threads()

logging.info("Finished scrapping")
logging.info("Storing to the DB")
if data:
    scrap = dict()
    scrap["streamers"] = data
    created_at = datetime.utcnow()
    scrap["created_at"] = created_at
    logging.info("Memory usage: %s" % memory_usage())
    try:
        Model.new_scrap(scrap)
        pass
    except Exception as e:
        logging.error("Data couldn't be saved in the DB. Logging exception.")
        logging.exception(e)
        backup_file = "%s/%s.dump" % (os.getenv("BACKUP"), created_at)
        backup_file = backup_file.replace(":", "-")
        with open(backup_file, 'wb') as bf:
            pickle.dump(scrap, bf, pickle.HIGHEST_PROTOCOL)
        logging.info("Data stored in file: %s.dump" % backup_file)
        # TODO: What if an exception raises during file writing? Sheeeeeeeeeeeeeeeeeeeeet
    else:
        logging.info("Data stored correctly")
else:
    logging.info("Data is empty. Nothing to save.")


Model.close()
