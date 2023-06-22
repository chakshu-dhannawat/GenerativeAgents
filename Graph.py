from Params import *
import heapq

# class Graph:

#   def __init__(self):
#     self.n = 0
#     self.graph = []
#     self.nodes = {}
#     self.places = []

#   def addNode(self,name):
#     self.graph.append([])
#     self.nodes[name] = self.n
#     self.places.append(name)
#     self.n += 1

#   def addEdge(self,n1,n2):
#     self.graph[self.nodes[n1]].append(self.nodes[n2])
#     self.graph[self.nodes[n2]].append(self.nodes[n1])

#   def getNodes(self,node):
#     return [self.places[n] for n in self.graph[self.nodes[node]]]

class Graph:
  
  def __init__(self):
    self.n = 0
    self.graph = {}
    
  def addNode(self,name):
    self.n+=1
    self.graph[name] = []
    
  def addEdge(self,n1,n2,weight=1):
    temp1 = (n2,weight)
    temp2 = (n1,weight)
    self.graph[n1].append(temp1)
    self.graph[n2].append(temp2)
    
  def shortestPath(self,start,end):
    distance = {node: float('inf') for node in graph}
    distance[start] = 0
    previous = {node: None for node in graph}
    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_node == end:
            break
        for neighbor, weight in graph[current_node]:
            distance_to_neighbor = current_distance + weight
            if distance_to_neighbor < distance[neighbor]:
                distance[neighbor] = distance_to_neighbor
                previous[neighbor] = current_node
                heapq.heappush(queue, (distance_to_neighbor, neighbor))
    path = []
    current_node = end
    while current_node is not None:
        path.insert(0, current_node)
        current_node = previous[current_node]

    return path
    
  

# Village Based Environment


places = list(nodes.keys())


def makeTown():

    town = Graph()    

    for node in places:
      town.addNode(node)

    town.addEdge("Tavern","Huts")
    town.addEdge("Tavern","Cattle Farm")
    town.addEdge("Tavern","Well")
    town.addEdge("Cattle Farm","Fishing Pond")
    town.addEdge("Cattle Farm","Shrine")
    town.addEdge("Well","Electricity House")
    town.addEdge("Well","Shrine")
    town.addEdge("Well","Huts")
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