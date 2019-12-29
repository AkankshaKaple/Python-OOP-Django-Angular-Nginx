import os


class Config:
    SECRET_KEY = os.environ['secretkey']
    class Mongodb:
        database_name = os.environ["database"],
        host = os.environ["dbhost"],
        port = os.environ["dbport"],
        username = os.environ["username"],
        password = os.environ["password"]

