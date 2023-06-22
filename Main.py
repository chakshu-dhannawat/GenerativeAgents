from Agent import Agent  
from Game import Game 
from Params import *
from Util import log
from datetime import datetime as dt

log("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
log(dt.now().strftime("%m/%d/%Y, %H:%M:%S"))

'''
====================
Initializing Agents
====================
'''
log('\n=======Initializing Agents=======\n')

graphics = [{'x':InitialPositions[i][0],'y':InitialPositions[i][1],'width':64, 'height':64, 'folder_name': f'character_0{i+1}'} for i in range(len(agentsDetails))] 

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
Warewolf Game
====================
'''
log('\n=======Warewolf Game=======\n')


night = 10*FPS
day = 20*FPS 
counter = 0

while game.run : 

    game.clock.tick(FPS)

    game.step()

    counter+=1
    if(counter==night):
      game.nightVote()
    if(counter==day):
      game.dayVote()
