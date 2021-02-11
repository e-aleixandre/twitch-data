# Imports
import logging
from typing import List, Set
import os
import requests
import threading


class Twitch:
    def __init__(self):
        # List of streamers
        # self.__streamers: Set[Streamer] = set()
        # Holding every needed url so its easier to maintain
        self.__urls = {
            "auth": "https://id.twitch.tv/oauth2/token",
            "streams": "https://api.twitch.tv/helix/streams",
            "chatters": "https://tmi.twitch.tv/group/user/%s/chatters"
        }
        # Auth headers: I no longer use a session as they aren't thread safe
        self.__headers = None

    def get_access_token(self, client_id: str, secret: str) -> None:
        data = {
            "client_id": client_id,
            "client_secret": secret,
            "grant_type": "client_credentials"
        }

        r = requests.post(self.__urls["auth"], data=data)
        response = r.json()

        try:
            token = response["access_token"]
            self.__headers = {
                "client-id": client_id,
                "Authorization": ("Bearer %s" % token)
            }
            logging.debug("Authorized correctly")
        except KeyError:
            message = response.get("message")
            if message is not None:
                logging.critical("Exception when authorizing: %s", response.get("message"))
            else:
                logging.critical("Exception when authorizing. No message returned.")

            exit(-1)

    def get_top_streamers(self, amount: int, language: str) -> List:
        # TODO: Query multiple languages and concatenate the results
        params = {
            "first": amount,
            "language": "es"
        }

        r = requests.get(self.__urls["streams"], params=params, headers=self.__headers)
        response = r.json()

        try:
            data = response["data"]
            return data
        except KeyError:
            status = response.get("status")

            if status is not None:
                logging.critical("Getting top streamers failed with status code %d", status)
            else:
                logging.critical("Getting top streamers failed with no status code")

            exit(-1)

    def get_current_chatters(self, streamer: str) -> List:
        r = requests.get(self.__urls["chatters"] % streamer)
        response = r.json()
        try:
            chatters = response["chatters"]
            chatters = chatters["vips"] + chatters["viewers"]
            return chatters
        except KeyError:
            status = response.get("status")
            if status is not None:
                logging.error("Error getting chatters of %s with a status code of %d", streamer, status)
            else:
                logging.error("Error getting chatters of %s with no status code", streamer)

        return []

    def is_live(self, streamer: str) -> bool:
        params = {
            "user_login": streamer
        }
        r = requests.get(self.__urls["streams"], params=params, headers=self.__headers)
        response = r.json()

        return len(response["data"]) != 0
