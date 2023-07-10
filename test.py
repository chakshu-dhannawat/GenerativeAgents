from GPT import GPT
import time

with open("Logs\\logs.txt", 'w') as file: pass

gpt = GPT()
print(gpt.query("What is the Capital of Japan"))
print(gpt.query("What is the Capital of India"))