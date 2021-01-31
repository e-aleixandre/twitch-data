from typing import Set


class Streamer:
    def __init__(self, name: str):
        self.name: str = name
        self.viewers: Set[str]

