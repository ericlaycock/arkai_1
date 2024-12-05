from openai import OpenAI
import json
api_dir = '/home/eric/garbage/CWT_FT/API_keys/apikeys.json'

with open(api_dir, 'r') as file:
    api_keys = json.load(file)
client = OpenAI(api_key=api_keys['developmentOnly'])


def monkey_chat(message):
    messages = [
            {"role": "system", "content": f"You are a man who has turned into a monkey. 
            You try to communicate your human thoughts, but you are becoming 
            increasingly more monkey-like in your speech and behaviour."},
            {"role": "user", "content": f"Do you prefer bananas or a stable career?"},
            {"role": "assistant", "content": f"Ooh ooh! Bananas! I like bananas! But stable career - me like money. No like stress. Me pick both!"},
            {"role": "user", "content": f"Why do you know so much about humans?"},
            {"role": "assistant", "content": f"Me have human brain! Remember words! But no want be human again. Monkey good!"},
            {"role": "user", "content": f"{message}"}
        ]

    completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0,
            max_tokens=100
        )
    return completion.choices[0].message.content.strip()

while True:
    message = input("\nYou: ")
    print("Monkey:", monkey_chat(message))
