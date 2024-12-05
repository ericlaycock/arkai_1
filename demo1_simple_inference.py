from openai import OpenAI
import json
api_dir = '/home/eric/garbage/CWT_FT/API_keys/apikeys.json'

with open(api_dir, 'r') as file:
    api_keys = json.load(file)
client = OpenAI(api_key=api_keys['developmentOnly'])


messages = [
        {"role": "system", "content": f"You translate English to German"},
        {"role": "user", "content": f"translate <Hello> in the context of <Hello there, friend.>"}
    ]

completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0,
        max_tokens=30
    )

print(completion.choices[0].message.content.strip())
