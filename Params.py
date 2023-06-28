'''
====================
Game
====================
'''

Path = "Assets\\"
Emoji_Path = "Assets\\emojis\\"
WIN_WIDTH = 1000
WIN_HEIGHT = 700
EMOJI_SIZE = (25,25)
FPS = 100

TavernRadius = 100

LOCATION_MAP = {'Hut 1':(228,280),'Hut 1 task01':(148,175),
                'Hut 2':(500,280),'Hut 2 task01':(471,179),
                'Hut 3':(414,452),'Hut 3 task01':(317,382),'Hut 3 task02':(433,352),
                'Shrine':(379,574),'Shrine task01':(331,659),'Shrine task02':(191,624),'Shrine task03':(219,526),'Shrine task04':(349,515),
                'Cattle Farm':(751,182),'Cattle Farm task01':(887,182),'Cattle Farm task02':(947,258),'Cattle Farm task03':(895,334),'Cattle Farm task04':(732,334),
                'Well':(543,469),'Well task01':(543,507),'Well task02':(501,527),'Well task03':(458,495),'Well task04':(494,450),
                'Electricity House':(107,429),'Electricity House task01':(75,510),'Electricity House task02':(26,438),'Electricity House task03':(64,363),'Electricity House task04':(152,363),
                'Tavern':(830,533),
                'Fishing Pond':(576,93),'Fishing Pond task01':(80,34),'Fishing Pond task02':(210,74),'Fishing Pond task03':(652,97),'Fishing Pond task04':(937,71),
                'Intermediate01':(599,197),'Intermediate02':(599,309),'Intermediate03':(708,426),'Intermediate04':(626,549),'Intermediate05':(477,587),
                'Intermediate06':(107,578),'Intermediate07':(228,439),'Intermediate08':(107,75),'Intermediate09':(301,97),'Intermediate10':(849,103),
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
        "Shrine": "A sacred place where townfolks can pay homage, meditate, or seek spiritual solace.",
        "Well task01": "Drawing water from the well and distributing it to the villagers.",
        "Well task02": "Ensuring the well is clean and free from any contamination.",
        "Well task03": "Repairing the pulley system or any damages to the well structure.",
        "Well task04": "Monitoring the water level and quality of the well.",
        "Cattle Farm task01": "Feeding the animals and ensuring they have enough water.",
        "Cattle Farm task02": "Cleaning the animal pens and maintaining their hygiene.",
        "Cattle Farm task03": "Milking the cows and collecting eggs from the chickens.",
        "Cattle Farm task04": "Repairing or maintaining the fences and structures in the farm.",
        "Electricity House task01": "Maintaining the electricity generator or power source.",
        "Electricity House task02": "Checking and repairing any electrical equipment or wiring.",
        "Electricity House task03": "Ensuring a stable power supply to the village.",
        "Electricity House task04": "Managing the distribution of electrical resources.",
        "Shrine task01": "Offering Rituals: Agents can perform regular rituals and offer prayers at the Shrine to seek divine guidance and protection for the village.",
        "Shrine task02": "Cleaning and Maintenance: Agents can ensure that the Shrine area is clean and well-maintained, including sweeping, removing debris, and maintaining the altar or sacred objects.",
        "Shrine task03": "Lighting and Incense: Agents can light candles or oil lamps and burn incense at the Shrine, creating a peaceful and spiritual atmosphere.",
        "Shrine task04": "Gathering Sacred Herbs: Agents can search for and gather specific herbs or flowers near the Shrine that are used for religious rituals or medicinal purposes.",
        "Hut 1 task01": "Maintaining the cleanliness and tidiness of the houses.",
        "Hut 2 task01": "Repairing any damages or leaks in the houses.",
        "Hut 3 task01": "Collecting firewood or fuel for heating and cooking.",
        "Hut 3 task02": "Checking on elderly or vulnerable villagers, providing assistance if needed.",
        "Fishing Pond task01": "Setting up and checking fishing nets or traps.",
        "Fishing Pond task02": "Casting lines and catching fish for the village's food supply.",
        "Fishing Pond task03": "Cleaning and preparing the caught fish for cooking.",
        "Fishing Pond task04": "Maintaining the fishing equipment and repairing any damages.",
        "Intermediate01":"Inbetween Nodes",
        "Intermediate02":"Inbetween Nodes",
        "Intermediate03":"Inbetween Nodes",
        "Intermediate04":"Inbetween Nodes",
        "Intermediate05":"Inbetween Nodes",
        "Intermediate06":"Inbetween Nodes",
        "Intermediate07":"Inbetween Nodes",
        "Intermediate08":"Inbetween Nodes",
        "Intermediate09":"Inbetween Nodes",
        "Intermediate10":"Inbetween Nodes",
        }

hubs = [x for x in nodes.keys() if "task" not in x] 


'''
====================
Agents
====================
'''

MinDialogues = 1

agentsDetails = [
    {"name": "Takeshi Yamamoto", "description": "Takeshi is a warewolf; Takeshi is smart and is good at lying."},
    {"name": "Hiroshi Tanaka", "description": "Hiroshi is a townfolk; Hiroshi gets easily convinced from other's arguments."},
    {"name": "Aya Suzuki", "description": "Aya is a townfolk; Aya is smart and has good deduction skills."},
    # {"name": "Sakura Kobayashi", "description": "Sakura is a townfolk; Sakura is analytical."},
    # {"name": "Yumi Kimura", "description": "Yumi is a warewolf; Yumi is very smart."},
    # {"name": "Kaito Sato", "description": "Kaito is a townfolk; Kaito is dumb."},
    # {"name": "Akiko Tanaka", "description": "Akiko is a townfolk; Akiko has good convincing skills."},
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
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
