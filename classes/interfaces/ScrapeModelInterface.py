from abc import ABC, abstractmethod


class ScrapeModelInterface(ABC):
    """
    Interface for implementing different database services that will interact with a NOSQL kind of database
    for storing and retrieving scrapes
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def _check(self):
        pass

    @abstractmethod
    def new_scrap(self, scrap: dict):
        pass

    @abstractmethod
    def get_scraps(self, min_date, max_date):
        pass

    @abstractmethod
    def get_streamers(self, limit=0):
        pass

    @abstractmethod
    def close(self):
        pass
