import os
from typing import List

import psycopg2

# DB_USER = os.getenv("DB_USER", "")
# DB_PASSWORD = os.getenv("DB_PASSWORD", "")
# DB_HOST = os.getenv("DB_HOST", "")
# DB_PORT = os.getenv("DB_PORT", "")
# DB_NAME = os.getenv("DB_NAME", "")

DB_USER = "postgres"
DB_PASSWORD = "secret"
DB_HOST = "db"
DB_PORT = "5432"
DB_NAME = "postgres"

CONN_STR = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class DatabaseConnector:
    def __init__(self, conn_string: str = CONN_STR):
        self.conn_string = conn_string
        print(conn_string)

    def select(self, query: str) -> List[tuple]:
        with psycopg2.connect(self.conn_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()

    def execute(self, query: str) -> None:
        with psycopg2.connect(self.conn_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                conn.commit()



