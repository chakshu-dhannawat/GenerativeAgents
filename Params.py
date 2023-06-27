'''
====================
Game
====================
'''

Path = "Assets\\"

WIN_WIDTH = 1000
WIN_HEIGHT = 700

FPS = 100

TavernRadius = 100

LOCATION_MAP = {'Hut 1':(140,180),'Hut 1 task01':(141,246),
                'Hut 2':(435,210),'Hut 2 task01':(368,159),
                'Hut 3':(369,390),'Hut 3 task01':(426,349),'Hut 3 task02':(336,436),
                'Shrine':(285,610),'Shrine task01':(370,557),'Shrine task02':(200,526),'Shrine task03':(376,658),'Shrine task04':(148,602),
                'Cattle Farm':(867,254),'Cattle Farm task01':(781,327),'Cattle Farm task02':(917,310),'Cattle Farm task03':(914,152),'Cattle Farm task04':(759,168),
                'Well':(534,452),'Well task01':(446,497),'Well task02':(494,529),'Well task03':(548,513),'Well task04':(458,465),
                'Electricity House':(117,4.39),'Electricity House task01':(34,478),'Electricity House task02':(77,357),'Electricity House task03':(190,427),'Electricity House task04':(184,477),
                'Tavern':(810,550),
                'Fishing Pond':(576,45),'Fishing Pond task01':(262,70),'Fishing Pond task02':(111,48),'Fishing Pond task03':(637,89),'Fishing Pond task04':(927,66),
                }
MESSAGES_MAP = ["Hello!","How are you?",'Anata wa kawaii desu','Watashi wa Takeshi Desu','Hajimemashite','Otsukaresama deshita']

Locations = ['Hut 1','Hut 2','Hut 3','Shrine','Well','Shrine','Shrine']
InitialPositions = [LOCATION_MAP[loc] for loc in Locations]


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

nodes = {"Hut 1": "The first hut",
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

MinDialogues = 5

agentsDetails = [
    {"name": "Takeshi Yamamoto", "description": "Takeshi is a warewolf; Takeshi is smart and is good at lying."},
    {"name": "Hiroshi Tanaka", "description": "Hiroshi is a townfolk; Hiroshi gets easily convinced from other's arguments."},
    {"name": "Aya Suzuki", "description": "Aya is a townfolk; Aya is smart and has good deduction skills."},
    {"name": "Sakura Kobayashi", "description": "Sakura is a townfolk; Sakura is analytical."},
    {"name": "Yumi Kimura", "description": "Yumi is a warewolf; Yumi is very smart."},
    {"name": "Kaito Sato", "description": "Kaito is a townfolk; Kaito is dumb."},
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