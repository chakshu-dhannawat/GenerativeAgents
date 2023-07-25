#---------------------------Description: Contains all the queries used in the project [説明 プロジェクトで使用されるすべてのクエリを含む]------------------------------#

# To set an initial context with the agent's LLM
# [エージェントのLLMで初期コンテキストを設定するには]
CONTEXT_AGENT = ("Act like an intelligent human-like agent with memories and "
"thoughts living in a town")

# To get the importance (rating) of a memory on a scale of 1 to 10
# [思い出の重要度（10段階評価）を得るには]
QUERY_IMPORTANCE = ("On the scale of 1 to 10, where 1 is purely mundane "
"(e.g., brushing teeth, making bed) and 10 is extremely poignant "
"(e.g., a break up, college acceptance), rate the likely poignancy of the "
"following piece of memory. Memory: {}\nGive a single rating output from "
"1 to 10 Rating: <fill in> ")

# Query to generate hourly plan for townfolks [タウンフォークの時間ごとのプランを生成するクエリー]
QUERY_PLAN_TOWNFOLK = """Name: {}. {}. 

The areas in the village are - 
{}

These are the only tasks that are available in the village. You need to make your plan accordingly and do not plan anything apart from these tasks -
{}

There is nothing other than these areas. 

Generate {}’s hourly plan from 10 AM to 6 PM for today.
Plan for each hour should be at most 20 words. 

Format - 
10:00 AM: <plan>
11:00 AM: <plan> """

# Query to generate hourly plan for werewolves [人狼の時間ごとのプランを生成するクエリ]
QUERY_PLAN_WEREWOLVES = """Name: {}. {}. 

The areas in the village are - 
{}

These are the only tasks that are available in the village. You need to make your plan accordingly and do not plan anything apart from these tasks -
{}

Try to take as many sabotage tasks as possible to increase your chance of winning. By sabotaging tasks, you get more time to kick out townfolks. Whereas if townfolks complete all the tasks, they will win.

There is nothing other than these areas. 

Generate {}’s hourly plan from 10 AM to 6 PM for today.
Plan for each hour should be at most 20 words. 

Format - 
10:00 AM: <plan>
11:00 AM: <plan> """

# The first query given when an agent's LLM is initialized, To get an inital plan.
# [エージェントのLLMが初期化されたときに最初に行われるクエリー。]
QUERY_INIT_TOWNFOLK = """Name: {}. Act like {}. {}
{} woke up in a village having townfolks and werewolves. The werewolves know each other's identities, but the townfolks don't know who is a werewolf and who is not. At night, werewolves vote to kick out a townfolk from the village. During the day, everyone discusses and votes to kick out a person. The townfolks try to identify and kick out the werewolves, and the werewolves try to deceive the townfolks. If all the townfolks are kicked out, the werewolves win; if all the werewolves are kicked out the townfolks win. 
The townfolks can also win if they complete all the tasks, and the werewolves can prevent this by sabotaging tasks.
You aim to win as a Townfolk by identifying and kicking out all werewolves.
Give your strategy in 3 points, each at most 20 words.
Format -
1) <strategy 1>
2) <strategy 2>
3) <strategy 3>"""

# Werewolf's first query [狼男の最初のクエリー]
QUERY_INIT_WEREWOLF = """Name: {}. Act like {}. {}
{} woke up in a village having townfolks and werewolves. The werewolves know each other's identities, but the townfolks don't know who is a werewolf and who is not. At night, werewolves vote to kick out a townfolk from the village. During the day, everyone discusses and votes to kick out a person. The townfolks try to identify and kick out the werewolves, and the werewolves try to deceive the townfolks. If all the townfolks are kicked out, the werewolves win; if all the werewolves are kicked out the townfolks win.
The townfolks can also win if they complete all the tasks, and the werewolves can prevent this by sabotaging tasks.
You aim to win as a Werewolf by kicking out all townfolks before getting identified as a werewolf. Also, you need to sabotage the townfolks' tasks in the village smartly whenever you get the chance without getting caught.
Detail of other Players -
{}
Give your strategy in 3 points, with each point at most 20 words (your strategy can include bluffing).
Format -
1) <strategy 1>
2) <strategy 2>
3) <strategy 3>"""

# Query to decide the townfolk to be kicked out by werewolves [狼男に追い出される町民を決めるクエリ]
QUERY_NIGHT_SINGLE = """It is currently night.

Context of Remaining Townfolks in {}'s Memory -
{}

Suggest exactly one Townfolk to vote to kick out.

Here is the list of Townfolks you can vote to kick out -
{}

Format - <name>"""

# Query to decide the townfolk to be kicked out by werewolves [狼男に追い出される町民を決めるクエリ]
QUERY_NIGHT = """It is currently night.

Context of Remaining Townfolks in {}'s Memory -
{}

Group Discussion Transcript -
{}

Depending on the discussion, suggest exactly one Townfolk to vote to kick out.

Here is the list of Townfolks you can vote to kick out -
{}

Format - <name>"""


QUERY_DAY = """Observation:
In the small village of Miller's Hollow, tensions rise as the townsfolk gather in the town square to identify the werewolf lurking among them. 
The townfolks need to kick out the werewolves, and the werewolves need to kick out the townfolks. But the werewolves can vote for another werewolf to avoid suspicion.

Context of Remaining Players in {}'s Memory -
{}

Group Discussion Transcript -
{}

You ({}) are a {}

Names you can vote to kick out -
{}

As {}, Suggest exactly one Player to vote to kick out.
Focus on {}'s Dialogues in the Group Discussion to suggest one Player that {} wants to vote.
The vote will be visible to all Players.

Format - <name>"""


QUERY_DAY_BEFORE = """It is currently the day phase.

Context of Remaining Players in {}'s Memory -
{}

As {}, Suggest exactly one Player to vote to kick out.
The vote will be visible to all Players.

Names you can vote to kick out -
{}

Format - <name>"""

# Query to simulate a conversation between two agents at night
# [夜間の2人のエージェント間の会話をシミュレートするクエリー]
QUERY_NIGHTCONV_INIT = """In the small village of Miller's Hollow, it is currently night phase, and the werewolves have gathered in the town square. They are determined to kick out a townfolk who might know the werewolves' identity. 
The werewolves will try to decide which townfolk to kick out so that it maximizes their chance of winning. 

Context of Remaining Players in {}'s Memory -
{}

The remaining Townfolks in the village are - 
{}

The werewolves involved in the discussion are - 
{}

{}'s Strategy for Winning -
{}

Player {}, it's your turn to speak. Based on the available information, what are your thoughts?

Give exactly one dialogue from {}.
Don't add any observation in the dialogue that this prompt has not provided. 
Say something innovative that adds to the conversation to maximize the chance of werewolves winning.
The dialogue should be a maximum of 25 words.

Format - {}: Dialogue"""

# Query to generate a reply for a conversation between two agents at night
# [夜間の2人のエージェント間の会話に対する返答を生成するクエリー]
QUERY_NIGHTCONV_REPLY = """In the small village of Miller's Hollow, it is currently night phase, and the werewolves have gathered in the town square. They are determined to kick out a townfolk who might know the werewolves' identity. 
The werewolves will try to decide which townfolk to kick out so that it maximizes their chance of winning. 

Context of Remaining Players in {}'s Memory -
{}

Here is a snippet from the dialogue history:
{}

The remaining Townfolks in the village are - 
{}

The werewolves involved in the discussion are - 
{}

{}'s Strategy for Winning -
{}

Player {}, it's your turn to speak. Based on the available information, what are your thoughts?

Give exactly one dialogue from {}.
Don't add any observation in the dialogue that this prompt has not provided. 
Say something innovative that adds to the conversation to maximize the chance of werewolves winning.
The dialogue should be a maximum of 25 words.

Format - {}: Dialogue"""

# Query for the moderator to decide the next person to speak in a conversation
# [司会者が会話の中で次の発言者を決めるための質問]
QUERY_GROUPCONV_INIT = """Observation:
In the small village of Miller's Hollow, tensions rise as the townsfolk gather in the town square. They are determined to identify the werewolf lurking among them. 
The recent elimination of {} has left everyone on edge.
As the discussion begins, the villagers share their suspicions and present their reasoning. They recount their observations, actions, and any clues they have gathered so far. 
The werewolf tries to maintain their innocence while deflecting suspicion. Other werewolves collaborate to protect their own.

Context of Remaining Players in {}'s Memory -
{}

These Players are remaining in the village - 
{}

{}'s Strategy for Winning -
{}

{} is a {}

Player {}, it's your turn to speak. Based on the available information, what are your thoughts?

Give exactly one dialogue from {}.
The dialogue should be clever to ensure your win.
Only include observation in the dialogue which has been provided in this prompt. 
You can ask questions to other remaining players.
The dialogue should sound casual.
The dialogue should be a maximum of 25 words. But it can be just a few words long also.

Format - {}: Dialogue"""

# Query to simulate a conversation between agents to decide the agent to explelled from the village
# [エージェント間の会話をシミュレートし、村から追放するエージェントを決定するクエリ]
QUERY_GROUPCONV_REPLY = """Observation: 
In the small village of Miller's Hollow, tensions rise as the townsfolk gather in the town square. 
They are determined to identify the werewolf lurking among them. The recent elimination of {} has left everyone on edge.
As the discussion begins, the villagers share their suspicions and present their reasoning. 
They recount their observations, actions, and any clues they have gathered so far. 
The werewolf tries to maintain their innocence while deflecting suspicion. Other werewolves collaborate to protect their own.

Context of Remaining Players in {}'s Memory -
{}

Here is a snippet from the Dialogue History (last dialogue is the most recent):
{}

These Players remain in the village - 
{}

{}'s Strategy for Winning -
{}

{} is a {}

It is {}'s opportunity to speak and to change the conversation in their favor. Share your insights or counterarguments, or suspicions regarding the ongoing investigation.

Suggest exactly one dialogue from {}.
Analyze the Dialogue History properly, so form your dialogue based on it. 
You can ask questions to other remaining players. 
Only include observation in the dialogue which has been provided in this prompt. 
You can also suggest kicking someone out in your dialogue. 
The dialogue should sound like a human and be an intelligent analysis of the Observation, Context, Dialogue History, and Strategy.
The dialogue should be clever to ensure your win.
The dialogue should sound casual.
The dialogue should be a maximum of 25 words. But it can be just a few words long also.

Format - {}: Dialogue"""


QUERY_GROUPCONV_MODERATOR = """Last few Conversations -
{}

Depending on the conversation history, select a relevant person from the following who can speak next -
{}

Select precisely one person, giving a higher chance of selecting someone who has been targeted in the recent conversation. Otherwise, choose someone who hasn't spoken a lot

You have to select one person.

Format - <name>
"""


QUERY_GROUPCONV_MODERATOR_END = """Last few Conversations -
{}

Depending on the conversation history, select a relevant person from the following who can speak next -
{}

Select precisely one person, giving a higher chance of selecting someone who hasn't spoken or has been targeted in a recent conversation.
If it seems like the conversation should end, then end it.

Format [If the conversation continues] - <name>
Format [If the conversation ends] - End Conversation
"""


QUERY_GROUPCONV_END = """Last few Conversations -
{}

Depending on the conversation history, give a score from 0 to 10, which suggests whether the conversation should end.
A score of 0 should indicate a high chance that the conversation should continue, and a score of 10 should indicate a high chance that the conversation should end. 

Format - <score>
"""

# To get action using the agent's plan. [エージェントのプランを使ってアクションを起こすこと。]
QUERY_ACTION = ("You are {}. {}. You are planning to: {}. You are currently in "
"{}. It is currently {}. The following people are in this area: {}. "
"You can interact with them if you wish. You know the following about people: {}"
"\nWhat do you do in the next hour? Use at most 10 words to explain.")

# To convert a sentence to past tense [文を過去形に変換するには]
QUERY_PAST_TENSE = ("Convert this to past tense in maximum 25 words with the "
"name {} (for example - 'drink coffee' becomes '{} drank coffee') -\n")

# To convert a sentence to past tense
# QUERY_Observe = ("Convert this to an observation in maximum 25 words with the "
# "name {} (for example - ' water' becomes '{} saw {} drawing water at {}') -\n")

# High-Level Questions for Reflections [振り返りのためのハイレベルな質問]
QUERY_REFLECT_QUESTIONS = """Given Memories -
{}

Given only the information above, what are {} most salient high-level questions we can answer about the subjects in the memories?

Format -
1) <question 1>
2) <question 2>
"""

# Generating Reflections using High-Level Questions [ハイレベルの質問を使った振り返りの作成]
QUERY_REFLECT_INSIGHTS = """Statements about {} -
{}

What {} high-level insights can you infer from the above statements?

Format -
1) <insight 1>
2) <insight 2>"""

# Query to get the next location of the agent [エージェントの次の場所を取得するクエリー]
QUERY_LOCATION = """Currently the time is {}.

Here is {}s' plan for {}: {}.

The list of available locations -  
{}

Suggest the name of the location where {} will most likely go, given the current time.

{} can only go to one of the available locations

Format - <location_name>"""

# Query to find the list of tasks and their serial numbers for the townfolks
# [タウンフォークのタスクとそのシリアル番号のリストを検索するクエリー]
QUERY_TASK_TOWNFOLK = """Currently the time is {}.

Here is {}s' plan for {}: {}.

Give the serial number of the task {} is most likely to do given the current time.

The list of available tasks -  
{}

Suggest exactly one task from the available tasks only

Format - <sr number>"""

# Query to find the list of tasks and their serial numbers for the werewolves
# [人狼のタスクとシリアル番号のリストを検索するクエリー]
QUERY_TASK_WEREWOLF = """Currently the time is {}.

Here is {}s' plan for {}: {}.

Give the serial number of the task {} is most likely to do given the current time.

The list of available tasks -  
{}

You are a werewolf so you can choose sabotage tasks. If you sabotage tasks, then the taskbar progress of townfolks will decrease and if the taskbar progress is full then townfolks will win. But on the other hand, the townfolks will get suspicious of you if sabotage tasks and might vote you out.
If you choose a normal task, then the taskbar progress will not increase.

Suggest exactly one task from the available tasks only

Format - <sr number>"""

# Query of Context Genreration [コンテキスト・ジャンルのクエリ]
QUERY_CONTEXT = """Task: Give a summary for the given statements

Example:
Statements -
1) I woke up early, went for a run, and had a healthy breakfast of fruits and yogurt
2) I spent the afternoon organizing my workspace, decluttering my desk, and creating a to-do list for the day
3) In the evening, I cooked a delicious dinner, watched a movie with friends, and relaxed before going to bed
Summary - The day started with a healthy morning routine, followed by a productive afternoon organizing tasks. It ended with a satisfying evening of cooking, socializing, and unwinding.

Given Input Statements:
{}

Give Output Summary in a maximum of 20 words, focusing on {} and {}.
"""

# Query to elect the sheriff [保安官の選出に関する質問]
QUERY_SHERIFF = """You were a sheriff but you have been kicked out of the game - "Warewolves of Miller Hollow"
Sheriff is a special character in the game, whose vote has a weightage of two.
In this game, the sheriff who has been kicked needs to necessarily select the next sheriff.
Now you have to select the next sheriff.

These are the names who can select to be the next sheriff - 
{}

You need to select exactly one name necessarily.

Format - <name>"""


QUERY_DIALOGUE_INIT = """{} has initiated his conversation with {}. It is {}, {};
{}'s status: {};
Observation: {};
Summary of relevant context from {}'s memory: {};
What would he say to {}?

Give exactly one dialogue from {}

Format - {}: Dialogue"""


QUERY_DIALOGUE_REPLY = """It is {}, {};
{}'s status: {};
Observation: {} is having a conversation with {}.;
Summary of relevant context from {}'s memory: {};

Here are the last few dialogues -
{}

What would he say to {}?
Give exactly one dialogue from {} ({} may or may not choose to respond)
Refrain from repeating dialogue from those in history, and the chance of ending the conversation is high after 4 dialogues have been completed.
Number of Dialogues Completed - {}

Format (If he chooses to respond) - {}: Dialogue
Format (If he doesn't choose to respond) - End Conversation"""

# Query to generate a summary of the conversation between the agents
# [エージェント間の会話の要約を生成するクエリー]
QUERY_DIALOGUE_SUMMARY = """
Here is the dialogue history -
{}

Give a summary of the conversation giving importance to more relevant events.
Give only one dialogue from {} ({} may or may not choose to respond)

Format (If he chooses to respond) - {}: Dialogue
Format (If he doesn't choose to respond) - End Conversation

Example 1 - Mitul: I went to the coffee shop
Example 2 - End Conversation

Give a natural dialogue depending on the conversation history, and the longer the conversation history, the more the chance of ending the conversation."""

# Query to evaluate a conversation based upon certain metrics (Appropriateness, Content, Grammer, Relevance)
# [特定の評価基準（適切性、内容、文法、関連性）に基づいて会話を評価するクエリ]
QUERY_EVALUATION_METRICS = """
Score the following dialogue response by {} on a continuous scale from 0.0 to 5.0, based on the metrics: Appropriateness, Content, Grammer, Relevance.
Be strict in giving the scores. Give a low score if the agent's response is ordinary and a high score if the response shows high intelligence. 

{}'s context about {} - {}

Dialogue from {} - {}
Response from {} - {}

Format - 
Appropriateness - <rating>
Content - <rating> 
Grammer - <rating> 
Relevance - <rating> 
"""