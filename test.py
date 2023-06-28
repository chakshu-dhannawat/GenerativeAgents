from Util import getTasks
from Graph import town 


nodes = town.graph["Cattle Farm"]
for node in nodes : 
    print(node)
    print("task" in node[0]) 
    print()

print(getTasks("Cattle Farm"))