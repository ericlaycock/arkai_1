from openai import OpenAI
import json

api_dir = '/home/eric/garbage/CWT_FT/API_keys/apikeys.json'
file_dir = "/home/eric/garbage/arkai/finetuning_data.jsonl"
# valid_file = "/home/eric/garbage/...development.jsonl"

with open(api_dir, 'r') as file:
    api_keys = json.load(file)
client = OpenAI(api_key=api_keys['developmentOnly'])


# valid1 = client.files.create(
#     file=open(valid_file,"rb"),
#     purpose="fine-tune")

response1 = client.files.create(
  file=open(file_dir, "rb"),
  purpose="fine-tune")
# Print the response to get the file ID
hyperparameters = {"batch_size": 1}
response = client.fine_tuning.jobs.create(
  hyperparameters=hyperparameters,
  training_file=response1.id,
  
  # validation_file=valid1.id,
  #gpt=4o-2024-08-06 ....... gpt-4o-mini-2024-07-18
  model="gpt-4o-mini-2024-07-18",
  suffix="testric"
)

print(response)