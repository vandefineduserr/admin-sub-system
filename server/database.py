from pymongo import MongoClient
from constants import CONNECTION_STRING

class DB:
    def connect(self):
        return MongoClient(CONNECTION_STRING)["ws-admin-system"]
    