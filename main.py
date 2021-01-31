# IMPORTS
import Twitch
import logging
import dotenv
import os

# LOADING ENV VARIABLES
dotenv.load_dotenv(".env.local")

# CONFIGURING THE LOGGER
logging.basicConfig(filename="twitch-data.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# STARTING
twitch = Twitch.Twitch()

logging.info("Started scrapping")
logging.info("Trying to get an authorization")
twitch.get_access_token(os.getenv("CLIENTID"), os.getenv("SECRET"))
logging.info("Fetching spanish top 2")
streams = twitch.get_top_streamers(2, "es")

"""
for stream in streams:
    username = stream["user_login"]
    logging.info("Getting chatters for %s" % username)
    chatters = Twitch.get_current_chatters(username)
    print(chatters)
"""

logging.info("Getting chatters for kuku0678")
chatters = twitch.get_current_chatters("kuku0678")