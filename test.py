# import openai
# import os

# openai.api_type = os.getenv('OpenAI_Type')

# openai.api_base = os.getenv('OpenAI_Base')

# openai.api_version = os.getenv('OpenAI_Version')

# openai.api_key = os.getenv("OpenAI_API_KEY")

# response = openai.Embedding.create(
#     input="Your text string goes here",
#     model="text-embedding-ada-002"
# )
# embeddings = response['data'][0]['embedding']
# print(embeddings)

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def calculate_word_count(response):
    return len(word_tokenize(response))

def calculate_information_density(response):
    word_count = calculate_word_count(response)
    stopwords_count = len([word for word in word_tokenize(response) if word.lower() in stopwords.words('english')])
    return (word_count - stopwords_count) / word_count

def calculate_sentiment(response):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(response)
    return sentiment_scores['compound']

def calculate_topic_coverage(response, relevant_topics):
    topic_count = sum([1 for topic in relevant_topics if topic.lower() in response.lower()])
    return topic_count / len(relevant_topics)

def calculate_readability(response):
    words = word_tokenize(response)
    total_words = len(words)
    total_sentences = len(nltk.sent_tokenize(response))
    total_syllables = sum([nltk.syllable_count(word) for word in words])
    return 0.39 * (total_words / total_sentences) + 11.8 * (total_syllables / total_words) - 15.59

# Example usage
response1 = "Entering politics in your 20s can provide valuable experience, networking opportunities, and a chance to bring fresh ideas."
response2 = "While politics in your 20s may have challenges, it can also offer the chance to advocate for important issues."

word_count1 = calculate_word_count(response1)
word_count2 = calculate_word_count(response2)

info_density1 = calculate_information_density(response1)
info_density2 = calculate_information_density(response2)

sentiment1 = calculate_sentiment(response1)
sentiment2 = calculate_sentiment(response2)

topic_coverage1 = calculate_topic_coverage(response1, ["advantages", "politics", "20s"])
topic_coverage2 = calculate_topic_coverage(response2, ["challenges", "politics", "20s"])

readability1 = calculate_readability(response1)
readability2 = calculate_readability(response2)

print("Response 1:")
print("Word Count:", word_count1)
print("Information Density:", info_density1)
print("Sentiment:", sentiment1)
print("Topic Coverage:", topic_coverage1)
print("Readability:", readability1)

print("\nResponse 2:")
print("Word Count:", word_count2)
print("Information Density:", info_density2)
print("Sentiment:", sentiment2)
print("Topic Coverage:", topic_coverage2)
print("Readability:", readability2)
