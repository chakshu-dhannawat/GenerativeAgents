from pymongo import MongoClient
from Memories import *
from Params import agentsDetails


client = MongoClient("mongodb+srv://harshagrawal1046:harsh1234@cluster0.3v5rngf.mongodb.net/?retryWrites=true&w=majority")


class DBHandler:
    def __init__(self):
        self.memoriesDB = client["memories_DB"]
        self.agentCollection = {}
        self.initDB()

    def initDB(self):
        collection_names = self.memoriesDB.list_collection_names()
        for collection in collection_names:
            self.memoriesDB[collection].drop()
        
        for agent in agentsDetails:
            self.agentCollection[agent["name"]]=self.memoriesDB[agent["name"]]


    def addMemories(self, name,observation,creation,lastAccess,importance):
        d = {'observation':observation,
            'creation':creation,
            'lastAccess':lastAccess,
            'importance':importance}
        self.agentCollection[name].insert_one(d)
    
    def getAllMemories(self, name):
        d = self.agentCollection[name].find()
        return d
DB = DBHandler()
DB.addMemories(agentsDetails[0]["name"], "Abcsn", "adkcsv", "sncjosnc", 0)