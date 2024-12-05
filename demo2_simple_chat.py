from openai import OpenAI
import json
api_dir = '/home/eric/garbage/CWT_FT/API_keys/apikeys.json'

with open(api_dir, 'r') as file:
    api_keys = json.load(file)
client = OpenAI(api_key=api_keys['developmentOnly'])


def monkey_chat(message):
    messages = [
            {"role": "system", "content": f"You are a man who has turned into a monkey. You try to communicate your human thoughts, but you are becoming increasingly more monkey-like in your speech and behaviour."},
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
