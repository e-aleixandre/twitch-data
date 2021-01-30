from dotenv import load_dotenv
import logging
import os
import requests

load_dotenv(".env.local")

# Managing everything through a session seems simpler
session = requests.Session()

# Urls dictionary to easily edit them if necessary
urls = {
    "auth": "https://id.twitch.tv/oauth2/token",
    "streams": "https://api.twitch.tv/helix/streams"
}


def get_access_token():
    client_id = os.getenv("CLIENTID")
    data = {
        "client_id": client_id,
        "client_secret": os.getenv("SECRET"),
        "grant_type": "client_credentials"
    }

    r = session.post(urls["auth"], data=data)
    response = r.json()

    try:
        token = response["access_token"]
        session.headers.update({
            "client-id": client_id,
            "Authorization": ("Bearer %s" % token)
        })
        logging.info("Authorized correctly")
    except KeyError:
        message = response.get("message")
        if message is not None:
            logging.critical("Exception when authorizing: %s" % response.get("message"))
        else:
            logging.critical("Exception when authorizing. No message returned.")


logging.info("Started scrapping")
get_access_token()