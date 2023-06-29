from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import re

from Queries import *

# --------------------------------------------------------------------------------
dialogue = """
Yumi Kimura: "I think we should focus on Kaito Sato, he seems suspicious to me. And we need to act fast if we want to win this game."
Hiroshi Tanaka: "I agree, Yumi. Kaito Sato's behavior has been erratic, and we need to be decisive in our actions."
Aya Suzuki: "I agree with Yumi and Hiroshi. Kaito Sato's behavior has been concerning. Let's keep a close eye on him and vote strategically."
Kaito Sato: "I don't know why you all think I'm suspicious. I'm just trying to do my best to help the townfolks win."
Akiko Tanaka: "I agree with Yumi, Hiroshi and Aya. We need to keep a close eye on Kaito Sato and gather more information before making a decision."
Yumi Kimura: "I'm glad we all agree that Kaito Sato is suspicious. Let's keep a close eye on him and gather more information before making a decision."
Hiroshi Tanaka: "I trust Takeshi's judgment, but I also see the point that Aya, Yumi, and Akiko are making about Kaito Sato. Let's gather more information before making a decision."
Yumi Kimura: "I agree with Hiroshi that we should trust Takeshi's judgment. But, we should also consider the suspicious behavior of Kaito Sato. Let's gather more information before making a decision."
Hiroshi Tanaka: "I agree with Aya, Yumi, and Akiko. We need to keep a close eye on Kaito Sato and gather more information before making a decision."
Aya Suzuki: "I agree with Hiroshi that we should trust Takeshi's judgment, but we should also keep in mind the suspicious behavior of Kaito Sato. Let's gather more information before making any decisions."
Kaito Sato: "I don't know who to trust. I'm just trying to analyze everyone's behavior, but it's all so confusing."
Akiko Tanaka: "I agree with Yumi and Hiroshi. We need to gather more information on Kaito Sato's behavior before making any decisions. Let's keep a close eye on him and observe his actions in the next round of voting."
Kaito Sato: "I don't know who to trust. I'm just trying to analyze everyone's behavior, but it's all so confusing. I hope we can gather more information and make the right decision."
Yumi Kimura: "I agree with Aya. We should keep an eye on Kaito's behavior and gather more information before making any decisions. However, I have a feeling that Takeshi's judgment may not be as trustworthy as we think."
Hiroshi Tanaka: "I agree with Akiko and Yumi. We should observe Kaito's behavior closely. However, I think Takeshi's opinion is valuable too. Maybe we can work together to gather more information and make the right decision."
"""


# Turn-taking ratio metric
def get_turn_taking_ratio(dialogue):
    agents = set([line.split(":")[0].strip() for line in dialogue.split("\n")])
    agent_turns = {agent: dialogue.count(agent + ":") for agent in agents}
    total_turns = sum(agent_turns.values())
    if total_turns == 0:
        return 0
    return {agent: turns / total_turns for agent, turns in agent_turns.items()}

turn_taking_ratio = get_turn_taking_ratio(dialogue)
print("Turn-taking ratio:", turn_taking_ratio)

# --------------------------------------------------------------------------------
 
# Response relevance metric
def calculate_response_relevance(dialogue):
    agents = []
    utterances = []

    lines = dialogue.strip().split("\n")

    for line in lines:
        parts = line.split(":")
        if len(parts) >= 2:
            agent = parts[0].strip()
            utterance = ":".join(parts[1:]).strip()
            agents.append(agent)
            utterances.append(utterance)

    num_utterances = len(utterances)

    if num_utterances < 2:
        return [0.0]

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(utterances)
    similarity_matrix = cosine_similarity(tfidf_matrix)

    response_relevance_scores = []
    
    total = 0
    for i in range(num_utterances):
        response_relevance = sum(similarity_matrix[i]) - similarity_matrix[i][i]
        response_relevance_scores.append(response_relevance)
        total += response_relevance

    return response_relevance_scores, total/num_utterances

# Example usage
response_relevance, avg = calculate_response_relevance(dialogue)
print("Response Relevance:", response_relevance)
print("Average Response Relevance:", avg)

# --------------------------------------------------------------------------------

# Conversation agreement metric
def calculate_agreement_metric(dialogue):
    agents = []
    utterances = []
    
    lines = dialogue.strip().split("\n")
    
    for line in lines:
        parts = line.split(":")
        if len(parts) >= 2:
            agent = parts[0].strip()
            utterance = ":".join(parts[1:]).strip()
            agents.append(agent)
            utterances.append(utterance)
    
    num_agents = len(agents)
    
    if num_agents < 2:
        return 0.0
    
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(utterances)
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    agreement = 0.0
    count = 0
    
    for i in range(num_agents):
        for j in range(i+1, num_agents):
            agreement += similarity_matrix[i][j]
            count += 1
    
    if count == 0:
        return 0.0
    
    agreement_metric = agreement / count
    return agreement_metric


agreement_metric = calculate_agreement_metric(dialogue)
print("Agreement Metric:", agreement_metric*10)