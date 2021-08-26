import pymysql.cursors
import secrets
from .interfaces.ReportsModelInterface import ReportsModelInterface


class PyMysqlReportsModel(ReportsModelInterface):

    def __init__(self, user: str, password: str, host: str, database: str, port: int = 3306):
        self.__con = pymysql.connect(user=user, password=password, host=host,
                                     port=port, database=database, cursorclass=pymysql.cursors.DictCursor)

    def set_progress(self, id: int, progress: float):
        self.__con.ping(reconnect=True)
        cursor = self.__con.cursor()

        query = "UPDATE reports SET progress = %s WHERE id = %s"
        data = (progress, id,)
        cursor.execute(query, data)
        cursor.close()

    def set_pid(self, id: int, pid: int):
        self.__con.ping(reconnect=True)
        cursor = self.__con.cursor()

        query = "UPDATE reports SET pid = %s WHERE id = %s"
        data = (pid, id,)
        cursor.execute(query, data)
        cursor.close()

    def set_filename(self, id: int, filename: str):
        self.__con.ping(reconnect=True)
        cursor = self.__con.cursor()
        query = "UPDATE reports SET filename = %s WHERE id = %s"
        data = (filename, id,)
        cursor.execute(query, data)
        cursor.close()

    def set_completed(self, id: int):
        self.__con.ping(reconnect=True)
        cursor = self.__con.cursor()
        query = "UPDATE reports SET completed = TRUE, progress = 100.0 WHERE id = %s"
        data = (id,)
        cursor.execute(query, data)
        cursor.close()

    def set_errored(self, id: int):
        self.__con.ping(reconnect=True)
        cursor = self.__con.cursor()
        query = "UPDATE reports SET errored = TRUE WHERE id = %s"
        data = (id,)
        cursor.execute(query, data)
        cursor.close()

    def set_notification_token(self, id: int) -> str:
        self.__con.ping(reconnect=True)
        cursor = self.__con.cursor()
        token = secrets.token_hex(nbytes=16)
        query = "UPDATE reports SET token = %s WHERE id = %s"
        data = (token, id,)
        cursor.execute(query, data)
        cursor.close()

        return token

    def close(self):
        if self.__con.open:
            self.__con.close()

    def commit(self):
        self.__con.commit()

