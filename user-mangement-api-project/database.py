import sqlite3
def get_connection():
    connection = sqlite3.connect("users.db")
    return connection