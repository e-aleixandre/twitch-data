from psycopg2 import connect

__con = None
__initialized = False


def initialize(constring: str):
    global __con
    global __initialized
    __con = connect(constring)
    __initialized = True


def set_progress(id: int, progress: float):
    global __con
    cursor = __con.cursor()

    query = "UPDATE reports SET progress = %s WHERE id = %s"
    data = (id, progress, )
    cursor.execute(query, data)
    __con.commit()
    cursor.close()


def set_pid(id: int, pid: int):
    global __con
    cursor = __con.cursor()

    query = "UPDATE reports SET pid = %s WHERE id = %s"
    data = (pid, id, )
    cursor.execute(query, data)
    __con.commit()
    cursor.close()


def set_completed(id: int, filename: str):
    global __con
    cursor = __con.cursor()
    query = "UPDATE reports SET completed = TRUE, \"fileName\" = %s, progress = 100.0 WHERE id = %s"
    data = (filename, id, )
    cursor.execute(query, data)
    __con.commit()
    cursor.close()


def set_errored(id: int):
    global __con
    cursor = __con.cursor()
    query = "UPDATE reports SET errored = TRUE WHERE id = %s"
    data = (id, )
    cursor.execute(query, data)
    __con.commit()
    cursor.close()


def close():
    global __con
    global __initialized
    if __initialized:
        __con.close()
