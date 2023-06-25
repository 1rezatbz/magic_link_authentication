from redis import StrictRedis
import sqlite3
from config import env_config


class RedisConnection:
    """
    This class provides a connection to Redis and basic operations on Redis.
    """

    _connection = None

    @classmethod
    def get_connection(cls):
        """
        Get the Redis connection. If the connection doesn't exist, create a new one.
        :return: Redis connection
        """
        if not cls._connection:
            cls._connection = StrictRedis()
        return cls._connection

    @classmethod
    def set_value(cls, key, value):
        """
        Set a value in Redis with the given key.
        :param key: Key for the value
        :param value: Value to be set
        """
        cls.get_connection().set(key, value)

    @classmethod
    def get_value(cls, key):
        """
        Get the value from Redis for the given key.
        :param key: Key to retrieve the value
        :return: Value for the key
        """
        return cls.get_connection().get(key)

    @classmethod
    def del_value(cls, key):
        """
        Delete the value from Redis for the given key.
        :param key: Key to delete the value
        :return: Number of keys deleted
        """
        return cls.get_connection().delete(key)


class SqlLiteConnection:
    """
    This class provides a connection to SQLite and basic operations on the database.
    """

    def __init__(self):
        self.db_name = env_config.sqlite_file
        self.conn = None
        self.cursor = None

    def connect(self):
        """
        Connect to the SQLite database.
        """
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        """
        Disconnect from the SQLite database.
        """
        if self.conn:
            self.conn.close()

    def execute(self, query, params=None):
        """
        Execute the SQL query on the SQLite database.
        :param query: SQL query to execute
        :param params: Parameters for the query
        """
        if not self.conn:
            self.connect()

        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

        self.conn.commit()

    def fetch_all(self):
        """
        Fetch all rows from the result of the last executed query.
        :return: All rows as a list of tuples
        """
        return self.cursor.fetchall()

    def fetch_one(self):
        """
        Fetch one row from the result of the last executed query.
        :return: One row as a tuple
        """
        return self.cursor.fetchone()
