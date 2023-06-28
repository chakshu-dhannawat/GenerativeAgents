# To set an initial context with the agent's llm
CONTEXT_AGENT = ("Act like an intelligent human like agent with memories and "
"thoughts living in a town")

# To get the importance (rating) of a memory on a scale of 1 to 10
QUERY_IMPORTANCE = ("On the scale of 1 to 10, where 1 is purely mundane "
"(e.g., brushing teeth, making bed) and 10 is extremely poignant "
"(e.g., a break up, college acceptance), rate the likely poignancy of the "
"following piece of memory. Memory: {}\nGive a single rating output from "
"1 to 10 Rating: <fill in> ")

QUERY_PLAN = """Name: {}. {}. 

The areas in the village are - 
{}

There is nothing other than these areas. 

Generate {}’s hourly plan from 10 AM to 6 PM for today.
Plan for each hour should not be more than 20 words. 

Format - 
10:00 AM: <plan>
11:00 AM: <plan> """

# The first query given when an agent's llm is initialized, To get an inital plan.
QUERY_INIT_TOWNFOLK = """Name: {}. Act like {}. {}
{} woke up in a village having townfolks and warewolves. The warewolves know each other's identity, but the townfolfs don't know who is warewolf and who is not. During the night warewolves vote to kick out a townfolk from the village. During the day, everyone have a discussion and vote to kick out a person. The townfolks try to identify and kick out the warewolves, and the warewolves try to decieve the townfolks. If all the townfolks are kicked out, the warewolves win, and if all the warewolves are kicked out the townfolks win.
Your objective is to win as a Townfolk by identifying and kicking out all warewolves.
Give your strategy in 3 points, with each point not more than 20 words.
Format -
1) <strategy 1>
2) <strategy 2>
3) <strategy 3>"""

QUERY_INIT_WAREWOLF = """Name: {}. Act like {}. {}
{} woke up in a village having townfolks and warewolves. The warewolves know each other's identity, but the townfolfs don't know who is warewolf and who is not. During the night warewolves vote to kick out a townfolk from the village. During the day, everyone have a discussion and vote to kick out a person. The townfolks try to identify and kick out the warewolves, and the warewolves try to decieve the townfolks. If all the townfolks are kicked out, the warewolves win, and if all the warewolves are kicked out the townfolks win.
Your objective is to win as a Warewolf by kicking out all townfolks before getting identified as a warewolf.
Detail of other Players -
{}
Give your strategy in 3 points, with each point not more than 20 words (your strategy can include things like bluffing).
Format -
1) <strategy 1>
2) <strategy 2>
3) <strategy 3>"""

QUERY_NIGHT = """It is currently night.
Context of Remaining Townfolks in {}'s Memory -
{}
Select exactly one Townfolk to vote to kick out.
Format - <serial number>
Example - 2)"""

QUERY_DAY = """It is currently day.

Context of Remaining Players in {}'s Memory -
{}

Group Discussion -
{}

As {}, Select exactly one Player to vote to kick out.
The vote will be visible to all Players.

Names you can vote to kick out -
{}

Format - <name>"""


# QUERY_GROUPCONV_INIT = """The villagers gather at the town square for a heated discussion. The motive of this discussion is to identify and eliminate the werewolf among them. The townsfolks will deliberate on who they believe is the werewolf, the werewolf will attempt to defend their innocence, trying to deflect suspicion away from themselves. Other werewolves help each other in trying to avoid elimination of their fellow werewolves, and instead get a townfolk eliminated.
# Observation: Yesterday the Warewolves kicked out {}.

# Context of Remaining Players in {}'s Memory -
# {}

# What would {} say?

# Give exactly one dialogue from {}

# Format - {}: Dialogue"""

QUERY_GROUPCONV_INIT = """
Observation:
In the small village of Miller's Hollow, tensions rise as the townsfolk gather in the town square. They are determined to identify the werewolf lurking among them. 
The recent elimination of {} has left everyone on edge.
As the discussion begins, the villagers share their suspicions and present their reasoning. They recount their observations, actions, and any clues they have gathered so far. 
The werewolf tries to maintain their innocence while deflecting suspicion. Other werewolves collaborate to protect their own.

Context of Remaining Players in {}'s Memory -
{}

Player {}, it's your turn to speak. Based on the available information, what are your thoughts?

Give exactly one dialogue from {}.
The dialogue should be on point, instead of saying you agree with someone, say what you want to add to the conversation.
The dialogue should be of maximum 25 words.

Format - {}: Dialogue"""



# QUERY_GROUPCONV_REPLY = """Observation: Yesterday the Warewolves kicked out {}.

# Context of Remaining Players in {}'s Memory -
# {}

# Here is the dialogue history -
# {}

# What would {} say?

# Give exactly one dialogue from {}

# Format - {}: Dialogue"""


QUERY_GROUPCONV_REPLY = """Observation: 
In the small village of Miller's Hollow, tensions rise as the townsfolk gather in the town square. 
They are determined to identify the werewolf lurking among them. The recent elimination of {} has left everyone on edge.
As the discussion begins, the villagers share their suspicions and present their reasoning. 
They recount their observations, actions, and any clues they have gathered so far. 
The werewolf tries to maintain their innocence while deflecting suspicion. Other werewolves collaborate to protect their own.

Context of Remaining Players in {}'s Memory -
{}

Here is a snippet from the dialogue history:
{}

Player {}, now it's your opportunity to contribute. Share your insights, counterarguments, or suspicions regarding the ongoing investigation.

Give exactly one dialogue from {}.
The dialogue should be on point, instead of saying you agree with someone, say what you want to add to the conversation.
The dialogue should be of maximum 25 words.

Format - {}: Dialogue"""


QUERY_GROUPCONV_MODERATOR = """Last few Conversations -
{}

Depending on the conversation history, select a relevant person from the following who can speak next -
{}

Select exactly one person, give higher chance of selecting someone who has been targeted in the recent conversation, otherwise select someone who hasn't spoken a lot

You have to select one person.

Format - <name>
"""

QUERY_GROUPCONV_MODERATOR_END = """Last few Conversations -
{}

Depending on the conversation history, select a relevant person from the following who can speak next -
{}

Select exactly one person, give higher chance of selecting someone who hasnt spoken or has been targeted in the recent conversation.
If it seems like the conversation should end from the last few conversations, then end it.

Format [If conversation continues] - <name>
Format [If conversation ends] - End Conversation
"""

# To get action using the agent's plan.
QUERY_ACTION = ("You are {}. {}. You are planning to: {}. You are currently in "
"{}. It is currently {}. The following people are in this area: {}. "
"You can interact with them if you wish. You know the following about people: {}"
"\nWhat do you do in the next hour? Use at most 10 words to explain.")

# To convert a sentence to past tense
QUERY_PAST_TENSE = ("Convert this to past tense in maximum 25 words with the "
"name {} (for example - 'drink coffee' becomes '{} drank coffee') -\n")

# High-Level Questions for Reflections
QUERY_REFLECT_QUESTIONS = """Given Memories -
{}

Given only the information above, what are {} most salient high-level questions we can answer about the subjects in the memories?

Format -
1) <question 1>
2) <question 2>
"""

# Generating Reflections using High-Level Questions
QUERY_REFLECT_INSIGHTS = """Statements about {} -
{}

What {} high-level insights can you infer from the above statements?

Format -
1) <insight 1>
2) <insight 2>"""

# TODO (because of 1, 5, 3)) in format and add it to class also

# For rating locations
QUERY_LOCATION = """Currently the time is {}.
Here is {}s' hourly plan: 
{}.
On a scale of 1 to 10, where 1 indicates least likely to be in that location and 10 indicates most likely to be in that location, how likely is {} to go to {}.
Description of {}: {}

Give a single integer rating from 1 to 10."""

QUERY_CONTEXT = """Task: Give a summary for the given statements

Example:
Statements -
1) I woke up early, went for a run, and had a healthy breakfast of fruits and yogurt
2) I spent the afternoon organizing my workspace, decluttering my desk, and creating a to-do list for the day
3) In the evening, I cooked a delicious dinner, watched a movie with friends, and relaxed before going to bed
Summary - The day started with a healthy morning routine, followed by a productive afternoon organizing tasks. It ended with a satisfying evening of cooking, socializing, and unwinding.

Given Input Statements:
{}

Give Output Summary in maximum 20 words, focusing on {} and {}.
"""

QUERY_DIALOGUE_INIT = """{} has initiatiated his conversation with {}. It is {}, {};
{}'s status: {};
Observation: {};
Summary of relevant context from {}'s memory: {};
What would he say to {}?

Give exactly one dialogue from {}

Format - {}: Dialogue"""

QUERY_DIALOGUE_REPLY = """It is {}, {};
{}'s status: {};
Observation: {} has initiatiated conversation with {}.;
Summary of relevant context from {}'s memory: {};

Here is the dialogue history -
{}

What would he say to {}?
Give exactly one dialogue from {} ({} may or may not choose to respond)
Don't repeat dialogue from those in history, and chance of ending conversation is high after 4 dialogues in history.

Format (If he chooses to respond) - {}: Dialogue
Format (If he dosent choose to respond) - End Conversation"""

QUERY_DIALOGUE_SUMMARY = """
Here is the dialogue history -
{}

Give a summary of the conversation giving importance to more relevant events
Give only one dialogue from {} ({} may or may not choose to respond)

Format (If he chooses to respond) - {}: Dialogue
Format (If he dosent choose to respond) - End Conversation

Example 1 - Mitul: I went to the coffee shop
Example 2 - End Conversation

Give a natural dialogue depending on the conversation history, and longer the conversation history, more the chance of ending conversation."""

# TODO: Replace 'name' with actual name
# TODO: Add 2-3 reflections of conversation instead of exact conversations

# TODO: If conversation not ending then keep check on its length, otherwise exponentially tokens consume.....(maybe feed last 5 conversations only)
# TODO: No two location same rating

# TODO: Generate reflections of conversation after every 5-10 conversations
# TODO: also mention if warewolf/townfolk in vote query

# TODO: pass that line in first conv of each agent in group conv
# TODO: pass strategy in reply (or summary of strategy)

# TODO: Improve ExtractQuestions or use library
# TODO: Give info of how many warewolves and townfolks remaining always. Give info if the one lynched was warewolf or townfolk

# TODO: If only 2 dialogues in moderator then give how many dialogues each person has spoken also separately
# TODO: Add bluff in warewolves

# TODO: Add the observations to the agent's memories and also dialogue context and reflect also

# QUERY_DIALOGUE_REPLY = ("It is {}, {}; {}'s status: {}; Observation: {} has initiatiated "
# "conversation with {}.; Summary of relevant context from {}'s memory: {};\n\nHere is "
# "the dialogue history -\n{}\n\nWhat would he say to {}?\nGive only one dialogue "
# "from {} ({} may or may not choose to respond)")