'''
====================
Game
====================
'''

Path = "Assets\\"

WIN_WIDTH = 1000
WIN_HEIGHT = 700

FPS = 30

LOCATION_MAP = {'Hut 1':(140,180),'Hut 2':(350,190),'Hut 3':(350,350),'Shrine':(250,500),'Cattle Farm':(800,200),'Well':(500,450),'Electricity House':(110,370),'Taveren':(800,500),'Fishing Pond':(500,60)}
MESSAGES_MAP = ["Hello!","How are you?",'Anata wa kawaii desu','Watashi wa Takeshi Desu','Hajimemashite','Otsukaresama deshita']

InitialPositions = [LOCATION_MAP['Hut 1'],LOCATION_MAP['Hut 2'],LOCATION_MAP['Hut 3'],LOCATION_MAP['Shrine'],LOCATION_MAP['Well'],LOCATION_MAP['Shrine'],LOCATION_MAP['Shrine']]


'''
====================
Retrieval Alpha
====================
'''

Alpha_Recency = 0.3
Alpha_Importance = 0
Alpha_Relevance = 0.8

'''
====================
Town
====================
'''

townName = "Mk 1 Village"
Initial = "Tavern"

nodes = {"Huts": "Area where the townfolks live",
        "Hut 1": "The first hut",
        "Hut 2": "The second hut",
        "Hut 3": "The third hut",
        "Well": "A water source providing clean and fresh water for the townfolks",
        "Tavern": "A lively place where townfolks can socialize, exchange information",
        "Electricity House": "generates and distributes electricity power to the town",
        "Cattle Farm": "A dedicated area where livestock is raised for milk, meat, or other dairy products",
        "Fishing Pond": "A designated spot for fishing activities",
        "Shrine": "A sacred place where townfolks can pay homage, meditate, or seek spiritual solace."
        }


'''
====================
Agents
====================
'''

MinDialogues = 15

agentsDetails = [
    {"name": "Takeshi Yamamoto", "description": "Takeshi is a warewolf; Takeshi is smart and is good at lying."},
    {"name": "Hiroshi Tanaka", "description": "Hiroshi is a townfolk; Hiroshi gets easily convinced from other's arguments."},
    # {"name": "Aya Suzuki", "description": "Aya is a townfolk; Aya is smart and has good deduction skills."},
    # {"name": "Sakura Kobayashi", "description": "Sakura is a townfolk; Sakura is analytical."},
    # {"name": "Yumi Kimura", "description": "Yumi is a warewolf; Yumi is very smart."},
    # {"name": "Kaito Sato", "description": "Kaito is a townfolk; Kaito is dumb."},
    # {"name": "Akiko Tanaka", "description": "Akiko is a townfolk; Akiko has good convincing skills."}
]


'''
====================
Others
====================
'''

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
CREAM = (255,203,164)