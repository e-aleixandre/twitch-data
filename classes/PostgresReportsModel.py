from psycopg2 import connect
from .interfaces.ReportsModelInterface import ReportsModelInterface


class PostgresReportsModel(ReportsModelInterface):

    def __init__(self, constring: str):
        self.__con = connect(constring)
        self.__initialized = True

    def set_progress(self, id: int, progress: float):
        cursor = self.__con.cursor()

        query = "UPDATE reports SET progress = %s WHERE id = %s"
        data = (id, progress,)
        cursor.execute(query, data)
        self.__con.commit()
        cursor.close()

    def set_pid(self, id: int, pid: int):
        cursor = self.__con.cursor()

        query = "UPDATE reports SET pid = %s WHERE id = %s"
        data = (pid, id,)
        cursor.execute(query, data)
        self.__con.commit()
        cursor.close()

    def set_completed(self, id: int, filename: str):
        cursor = self.__con.cursor()
        query = "UPDATE reports SET completed = TRUE, \"fileName\" = %s, progress = 100.0 WHERE id = %s"
        data = (filename, id,)
        cursor.execute(query, data)
        self.__con.commit()
        cursor.close()

    def set_errored(self, id: int):
        cursor = self.__con.cursor()
        query = "UPDATE reports SET errored = TRUE WHERE id = %s"
        data = (id,)
        cursor.execute(query, data)
        self.__con.commit()
        cursor.close()

    def close(self):
        if self.__initialized:
            self.__con.close()
