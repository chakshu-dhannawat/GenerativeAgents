import openai 
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_type = os.getenv('OpenAI_Type')

openai.api_base = os.getenv('OpenAI_Base')

openai.api_version = os.getenv('OpenAI_Version')

openai.api_key = os.getenv("OpenAI_API_KEY")

response = openai.Embedding.create(
    input="Your text string goes here",
    engine="text-embedding-ada-002" 
)

embeddings = response['data'][0]['embedding']

print(embeddings)
print(embeddings[0])
print(embeddings[-1])