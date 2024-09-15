from database.connector import DatabaseConnector
with open('./database/init_database.sql') as file:
    query = file.read()
    connector = DatabaseConnector()
    connector.execute(query)