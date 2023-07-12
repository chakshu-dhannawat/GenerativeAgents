from Util import *
from Params import *

hub = "Shrine"
tasksList = [node for node in nodes if "task" in node and hub in node and "Sabotage" not in TASK_EMOJI_MAP[node]] 
print(tasksList)