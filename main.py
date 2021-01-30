# IMPORTS
import Twitch
import logging

# Configuring the logger
logging.basicConfig(filename="twitch-data.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logging.info("Started scrapping")
logging.info("Trying to get an authorization")
Twitch.get_access_token()
logging.info("Fetching spanish top 5")
streams = Twitch.get_top_streamers(5, "es")
print(streams)