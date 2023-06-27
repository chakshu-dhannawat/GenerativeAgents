from Agent import Agent  
from Game import Game 
from Params import *
from Util import log
from datetime import datetime as dt
import threading
import time
from queue import Queue

log("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
log(dt.now().strftime("%m/%d/%Y, %H:%M:%S"))

'''
====================
Initializing Agents
====================
'''
log('\n=======Initializing Agents=======\n')

graphics = [{'x':InitialPositions[i][0],'y':InitialPositions[i][1],'width':64, 'height':64, 'folder_name': f'character_0{i+1}', 'initialLocation': Locations[i]} for i in range(len(agentsDetails))] 

agents = [Agent(agent['name'],agent['description'],graphics[i]) for i,agent in enumerate(agentsDetails)]


'''
====================
Initializing Game
====================
'''
log('\n=======Initializing Game=======\n')

game = Game(agents)


'''
====================
Adding Memories for Testing
====================
'''
log('\n=======Adding Memories=======\n')

# game.agents[0].remember("Takeshi went fishing with Hiroshi")
# game.agents[0].remember("Takeshi stole fish from bucket of Hiroshi")
# game.agents[1].remember("Hiroshi went fishing with Takeshi")
# game.agents[3].remember("Sakura saw Takeshi and Hiroshi Fishing")
# game.agents[3].remember("Sakura saw some fish getting missing from the bucket of Hiroshi")


'''
====================
Warewolf Game [LOGIC]
====================
'''
log('\n=======Warewolf Game=======\n')



def game_logic():

  time.sleep(1)

  day = False
  
  while game.run:
     
    game.switchPhase()
    
    if(day):
      game.dayVote()
    else:  
      game.nightVote()
    
    day = not day

'''
====================
Warewolf Game [GRAPHICS]
====================
'''


def render():

  while game.run : 

      game.clock.tick(FPS)

      game.step()


'''
====================
Running Game using Multi-Threading
====================
'''


render_thread = threading.Thread(target=render)
logic_thread = threading.Thread(target=game_logic)

render_thread.start()
logic_thread.start()
