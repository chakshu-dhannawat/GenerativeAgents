from pymongo import MongoClient
from Memories import *
from Params import agentsDetails


client = MongoClient("mongodb+srv://harshagrawal1046:harsh1234@cluster0.3v5rngf.mongodb.net/?retryWrites=true&w=majority")


class DBHandler:
    def __init__(self,databaseName):
        self.memoriesDB = client[databaseName]
        self.agentCollection = {}
        self.initDB()

    def initDB(self):
        collection_names = self.memoriesDB.list_collection_names()
        for collection in collection_names:
            self.memoriesDB[collection].drop()
        
        for agent in agentsDetails:
            self.agentCollection[agent["name"]]=self.memoriesDB[agent["name"]]


    def addMemories(self, name, memory):
        d = {'observation':mecmory.observation,
            'creation':memory.creation,
            'lastAccess':memory.lastAccess,
            'importance':memory.importane}
        self.agentCollection[name].insert_one(d)
    
    def getAllMemories(self, name):
        d = self.agentCollection[name].find()
        memories_list = []
        for item in d:
            memory = Memory()
            memory.observation = item['observation']
            memory.creation = item['creation']
            memory.lastAccess = item['lastAccess']
            memory.importance = item['importance']
            memories_list.append(memory)
        return memories_list
DB = DBHandler("memories_DB")