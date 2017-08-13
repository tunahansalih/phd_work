import logging
import sqlite3 as lite
import threading
import os


class DbLogger:
    logsTable = "logs_table"
    runKvStore = "run_kv_store"
    runMetaData = "run_meta_data"
    leafInfoTable = "leaf_info_table"
    runResultsTable = "run_results"
    log_db_path = os.path.join(os.getcwd(), "..\\tf_experiments\\logger.db")

    logFormatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    loggersDict = {}
    lock = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def print_log(log_file_name, log_string):
        print("Enter print_log")
        DbLogger.lock.acquire()
        if not (log_file_name in DbLogger.loggersDict):
            logger_object = logging.getLogger(log_file_name)
            handler = logging.FileHandler(log_file_name, mode="w")
            handler.setFormatter(DbLogger.logFormatter)
            logger_object.setLevel(level=logging.INFO)
            logger_object.addHandler(handler)
            DbLogger.loggersDict[log_file_name] = logger_object
        logger_object = DbLogger.loggersDict[log_file_name]
        logger_object.info(log_string)
        print(log_string)
        DbLogger.lock.release()
        print("Exit print_log")

    @staticmethod
    def get_run_id():
        print("Enter get_run_id")
        DbLogger.lock.acquire()
        con = lite.connect(DbLogger.log_db_path)
        curr_id = None
        with con:
            cur = con.cursor()
            cur.execute("SELECT MAX(RunId) + 1 AS CurrId FROM {0}".format(DbLogger.runMetaData))
            rows = cur.fetchall()
            for row in rows:
                if row[0] is None:
                    curr_id = 0
                else:
                    curr_id = row[0]
        DbLogger.lock.release()
        print("Exit get_run_id")
        return curr_id

    @staticmethod
    def log_bnn_explanation(runId, explanation_string):
        print("Enter log_bnn_explanation")
        DbLogger.lock.acquire()
        explanation_string = explanation_string.replace("'", "")
        con = lite.connect(DbLogger.log_db_path)
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO {0} VALUES({1},'{2}')".format(DbLogger.runMetaData, runId, explanation_string))
        DbLogger.lock.release()
        print("Exit log_bnn_explanation")

    @staticmethod
    def log_kv_store(kv_store_rows):
        print("Enter log_kv_store")
        DbLogger.lock.acquire()
        kv_store_rows_as_tuple = tuple(kv_store_rows)
        con = lite.connect(DbLogger.log_db_path)
        with con:
            cur = con.cursor()
            cur.executemany("INSERT INTO {0} VALUES(?, ?, ?, ?, ?)"
                            .format(DbLogger.runKvStore), kv_store_rows_as_tuple)
        DbLogger.lock.release()
        print("Exit log_kv_store")

    @staticmethod
    def log_into_log_table(log_table_rows):
        print("Enter log_into_log_table")
        DbLogger.lock.acquire()
        log_table_rows_as_tuple = tuple(log_table_rows)
        con = lite.connect(DbLogger.log_db_path)
        with con:
            cur = con.cursor()
            cur.executemany("INSERT INTO {0} VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
                            .format(DbLogger.logsTable), log_table_rows_as_tuple)
        DbLogger.lock.release()
        print("Exit log_into_log_table")

    @staticmethod
    def log_into_leaf_table(log_table_rows):
        print("Enter log_into_leaf_table")
        DbLogger.lock.acquire()
        log_table_rows_as_tuple = tuple(log_table_rows)
        con = lite.connect(DbLogger.log_db_path)
        with con:
            cur = con.cursor()
            cur.executemany("INSERT INTO {0} VALUES(?, ?, ?)"
                            .format(DbLogger.leafInfoTable), log_table_rows_as_tuple)
        DbLogger.lock.release()
        print("Exit log_into_leaf_table")

    @staticmethod
    def write_into_table(rows, table, col_count):
        print("Enter write_into_table")
        DbLogger.lock.acquire()
        rows_as_tuple = tuple(rows)
        con = lite.connect(DbLogger.log_db_path)
        with con:
            cur = con.cursor()
            insert_cmd = "INSERT INTO {0} VALUES(".format(table)
            for i in range(0, col_count):
                insert_cmd += "?"
                if i != col_count - 1:
                    insert_cmd += ", "
            insert_cmd += ")"
            cur.executemany(insert_cmd, rows_as_tuple)
        DbLogger.lock.release()
        print("Exit write_into_table")

    @staticmethod
    def does_rows_exist(columns_to_values, table):
        print("Enter does_rows_exist")
        DbLogger.lock.acquire()
        sql_command = "SELECT * FROM {0} WHERE ".format(table)
        for item in enumerate(columns_to_values.items()):
            index = item[0]
            col_name = item[1][0]
            value = item[1][1]
            sql_command += "{0} = {1}".format(col_name, value)
            if index != len(columns_to_values) - 1:
                sql_command += " AND "
        con = lite.connect(DbLogger.log_db_path)
        with con:
            cur = con.cursor()
            cur.execute(sql_command)
            rows = cur.fetchall()
            does_exist = len(rows) > 0
        DbLogger.lock.release()
        print("Exit does_rows_exist")
        return does_exist