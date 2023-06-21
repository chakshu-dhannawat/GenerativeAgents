from Params import *

class Graph:

  def __init__(self):
    self.n = 0
    self.graph = []
    self.nodes = {}
    self.places = []

  def addNode(self,name):
    self.graph.append([])
    self.nodes[name] = self.n
    self.places.append(name)
    self.n += 1

  def addEdge(self,n1,n2):
    self.graph[self.nodes[n1]].append(self.nodes[n2])
    self.graph[self.nodes[n2]].append(self.nodes[n1])

  def getNodes(self,node):
    return [self.places[n] for n in self.graph[self.nodes[node]]]
  

# Village Based Environment


places = list(nodes.keys())


def makeTown():

    town = Graph()    

    for node in places:
      town.addNode(node)

    town.addEdge("Tavern","Huts")
    town.addEdge("Tavern","Cattle Farm")
    town.addEdge("Tavern","Shrine")
    town.addEdge("Cattle Farm","Fishing Pond")
    town.addEdge("Cattle Farm","Well")
    town.addEdge("Shrine","Electricity House")
    town.addEdge("Shrine","Well")
    town.addEdge("Shrine","Huts")
    town.addEdge("Huts","Hut 1")
    town.addEdge("Huts","Hut 2")
    town.addEdge("Huts","Hut 3")

    return town

town = makeTown()

# for i,node in enumerate(town.graph):
#     print(places[i],end=':\t\t')
#     for n2 in node:
#       print(places[n2],end=", ")
#     print()