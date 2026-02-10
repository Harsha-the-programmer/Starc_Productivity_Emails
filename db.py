import mysql.connector
from config import DB_CONFIG

def get_connection():
    return mysql.connector.connect(
        **DB_CONFIG,
        autocommit=True
    )

def get_cursor(conn):
    return conn.cursor(dictionary=True, buffered=True)
