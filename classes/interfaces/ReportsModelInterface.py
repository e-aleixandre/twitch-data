from abc import ABC, abstractmethod
from datetime import datetime


class ReportsModelInterface(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def set_progress(self, id: int, progress: float):
        pass

    @abstractmethod
    def set_pid(self, id: int, pid: int):
        pass

    @abstractmethod
    def set_completed(self, id: int):
        pass

    @abstractmethod
    def set_errored(self, id: int):
        pass

    @abstractmethod
    def set_notification_token(self, id: int) -> str:
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def commit(self):
        pass
