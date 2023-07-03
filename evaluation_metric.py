from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import re

from Queries import *

# --------------------------------------------------------------------------------
dialogue = """
Mana Yoshida: "I saw Hina Sato near the well this morning. She was acting a bit suspicious. We should investigate her further."
Hina Sato: "I was at the well with Riku Mori, trying to refill water supplies. I didn't see anything unusual."
Riku Mori: "I observed Yumi Okada and Hina Sato at the well and tavern. Let's investigate Yumi Okada's recent actions further."
Taichi Kato: "We need to consider Riku Mori's actions and whereabouts. He might be collaborating with the werewolf."
Yumi Okada: "We should investigate Mana Yoshida's actions too. She might be deflecting suspicion by accusing Hina Sato."
Mana Yoshida: "I agree that Riku Mori's actions should be investigated. But we should also consider Yumi Okada's behavior."
Yumi Okada: "Let's not forget to investigate Yuria Shimizu's actions. She might be the werewolf's accomplice."
Hina Sato: "I think we should investigate Taichi Kato's actions as well. We don't have any information about him yet."
"""


# Turn-taking ratio metric
def get_turn_taking_ratio(dialogue):
    agents = set([line.split(":")[0].strip() for line in dialogue.split("\n")])
    agent_turns = {agent: dialogue.count(agent + ":") for agent in agents}
    total_turns = sum(agent_turns.values())
    if total_turns == 0:
        return 0
    return {agent: turns / total_turns for agent, turns in agent_turns.items()}

# turn_taking_ratio = get_turn_taking_ratio(dialogue)
# print("Turn-taking ratio:", turn_taking_ratio)

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
# response_relevance, avg = calculate_response_relevance(dialogue)
# print("Response Relevance:", response_relevance)
# print("Average Response Relevance:", avg)

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


# agreement_metric = calculate_agreement_metric(dialogue)
# print("Agreement Metric:", agreement_metric*10)