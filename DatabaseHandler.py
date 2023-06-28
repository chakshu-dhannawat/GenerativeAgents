from pymongo import MongoClient
from Memories import *
from Params import agentsDetails


client = MongoClient("mongodb+srv://harshagrawal1046:harsh1234@cluster0.3v5rngf.mongodb.net/?retryWrites=true&w=majority")

# Memories Databse
memoriesDB = client["memories_DB"]


def initDB():
    collection_names = memoriesDB.list_collection_names()
    for collection in collection_names:
        memoriesDB[collection].drop()
    agentCollection = {}   
    for agent in agentsDetails:
        agentCollection[agent["name"]]=memoriesDB[agent["name"]]


def addMemories(name,observation,creation,lastAccess,importance):
    d = {'observation':observation,
         'creation':creation,
         'lastAccess':lastAccess,
         'importance':importance
         }
    agentCollection[name].insert_one(d)
   
def getAllMemories(name):
    d = agentCollection[name].find()
    return d

