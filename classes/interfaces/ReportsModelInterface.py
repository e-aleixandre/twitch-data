from abc import ABC, abstractmethod


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
    def set_completed(self, id: int, filename: str):
        pass

    @abstractmethod
    def set_errored(self, id: int):
        pass

    @abstractmethod
    def close(self):
        pass
