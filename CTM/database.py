import os
import pymysql

def get_connection():
    connection=pymysql.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("MYSQL_ROOT_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        # port="",
        autocommit=False
    )
    return connection