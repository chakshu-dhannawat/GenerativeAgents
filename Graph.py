# This file contains the graph structure of the village environment. Also finds the shortest path between two nodes.

from Params import *
import heapq     

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

  # Find the shortest path between two nodes using Dijkstra's algorithm    
  def shortestPath(self,start,end):
    distance = {node: float('inf') for node in self.graph}
    distance[start] = 0
    previous = {node: None for node in self.graph}
    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_node == end:
            break
        for neighbor, weight in self.graph[current_node]:
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

# Create the graph structure of the village
def makeTown():

    town = Graph()    

    for node in places:
      town.addNode(node)

    town.addEdge("Cattle Farm","Cattle Farm task01"),
    town.addEdge("Cattle Farm task01","Cattle Farm task02"),
    town.addEdge("Cattle Farm task02","Cattle Farm task03"),
    town.addEdge("Cattle Farm task02","Cattle Farm task04"),
    town.addEdge("Cattle Farm","Intermediate06"),
    town.addEdge("Intermediate07","Fishing Pond"),
    town.addEdge("Fishing Pond","Fishing Pond task01"),
    town.addEdge("Fishing Pond","Fishing Pond task02"),
    town.addEdge("Fishing Pond task02","Fishing Pond task03"),
    town.addEdge("Fishing Pond task03","Fishing Pond task04"),
    town.addEdge("Intermediate06","Intermediate07"),
    town.addEdge("Intermediate09","Hut 2"),
    town.addEdge("Intermediate05","Intermediate09"),
    town.addEdge("Intermediate05","Intermediate06"),
    town.addEdge("Intermediate04","Intermediate05"),
    town.addEdge("Hut 1","Intermediate08"),
    town.addEdge("Intermediate04","Intermediate08"),
    town.addEdge("Intermediate04","Electricity House"),
    town.addEdge("Electricity House","Intermediate03"),
    town.addEdge("Electricity House","Electricity House task01"),
    town.addEdge("Electricity House task01","Electricity House task02"),
    town.addEdge("Electricity House task02","Electricity House task03"),
    town.addEdge("Electricity House task03","Electricity House task04"),
    town.addEdge("Shrine","Shrine task02"),
    town.addEdge("Shrine task01","Shrine task02"),
    town.addEdge("Shrine","Shrine task03"),
    town.addEdge("Shrine task03","Shrine task04"),
    town.addEdge("Shrine","Intermediate02"),
    town.addEdge("Intermediate02","Intermediate03"),
    town.addEdge("Intermediate01","Intermediate02"),
    town.addEdge("Well","Intermediate01"),
    town.addEdge("Well","Intermediate05"),
    town.addEdge("Well","Well task03"),
    town.addEdge("Well task01","Well task02"),
    town.addEdge("Well task02","Well task03"),
    town.addEdge("Intermediate01","Tavern"),
    town.addEdge("Tavern","Predetermined 01"),
    town.addEdge("Predetermined 02","Predetermined 01"),
    town.addEdge("Predetermined 02","Predetermined 03"),
    town.addEdge("Predetermined 03","Predetermined 04"),
    town.addEdge("Predetermined 04","Predetermined 05"),
    town.addEdge("Predetermined 05","Predetermined 06"),
    town.addEdge("Tavern","Predetermined 06"),
    town.addEdge("Hut 1 Main","Hut 1"),
    town.addEdge("Hut 1 Main","Hut 1 Intermediate01"),
    town.addEdge("Hut 1 Intermediate01","Hut 1 Intermediate02"),
    town.addEdge("Hut 1 Intermediate01","Hut 1 Intermediate02"),
    town.addEdge("Hut 1 Intermediate02","Hut 1 Intermediate03"),
    town.addEdge("Hut 1 Intermediate01","Hut 1 Intermediate04"),
    town.addEdge("Hut 1 Intermediate04","Hut 1 Intermediate05"),
    town.addEdge("Hut 1 task01","Hut 1 Intermediate03"),
    town.addEdge("Hut 1 SleepIntermediate01","Hut 1 Intermediate04"),
    town.addEdge("Hut 1 SleepIntermediate02","Hut 1 Intermediate05"),
    town.addEdge("Hut 1 SleepIntermediate01","Hut 1 Sleeping01"),
    town.addEdge("Hut 1 SleepIntermediate02","Hut 1 SleepIntermediate03"),
    town.addEdge("Hut 1 SleepIntermediate02","Hut 1 SleepIntermediate04"),
    town.addEdge("Hut 1 SleepIntermediate04","Hut 1 SleepIntermediate05"),
    town.addEdge("Hut 1 SleepIntermediate05","Hut 1 Sleeping04"),
    town.addEdge("Hut 1 SleepIntermediate04","Hut 1 Sleeping03"),
    town.addEdge("Hut 1 SleepIntermediate03","Hut 1 Sleeping02"),
    town.addEdge("Hut 1 Main","Hut 1 Intermediate06"),
    town.addEdge("Hut 1 Intermediate07","Hut 1 Intermediate06"),
    town.addEdge("Hut 1 task04","Hut 1 Intermediate07"),
    town.addEdge("Hut 2 Main","Hut 2"),
    town.addEdge("Hut 2 Main","Hut 2 Intermediate01"),
    town.addEdge("Hut 2 Intermediate01","Hut 2 Intermediate02"),
    town.addEdge("Hut 2 Intermediate01","Hut 2 Intermediate02"),
    town.addEdge("Hut 2 Intermediate02","Hut 2 Intermediate03"),
    town.addEdge("Hut 2 Intermediate01","Hut 2 Intermediate04"),
    town.addEdge("Hut 2 Intermediate04","Hut 2 Intermediate05"),
    town.addEdge("Hut 2 task01","Hut 2 Intermediate03"),
    town.addEdge("Hut 2 SleepIntermediate01","Hut 2 Intermediate04"),
    town.addEdge("Hut 2 SleepIntermediate02","Hut 2 Intermediate05"),
    town.addEdge("Hut 2 SleepIntermediate01","Hut 2 Sleeping01"),
    town.addEdge("Hut 2 SleepIntermediate02","Hut 2 SleepIntermediate03"),
    town.addEdge("Hut 2 SleepIntermediate02","Hut 2 SleepIntermediate04"),
    town.addEdge("Hut 2 SleepIntermediate04","Hut 2 SleepIntermediate05"),
    town.addEdge("Hut 2 SleepIntermediate05","Hut 2 Sleeping04"),
    town.addEdge("Hut 2 SleepIntermediate04","Hut 2 Sleeping03"),
    town.addEdge("Hut 2 SleepIntermediate03","Hut 2 Sleeping02"),
    town.addEdge("Hut 2 Main","Hut 2 Intermediate06"),
    town.addEdge("Hut 2 Intermediate07","Hut 2 Intermediate06"),
    town.addEdge("Hut 2 task04","Hut 2 Intermediate07"),
    town.addEdge("Intermediate02","List"),
    return town

town = makeTown()