from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.chains import SequentialChain, LLMChain
from langchain.prompts import PromptTemplate
import json
import re

with open('/home/eric/garbage/CWT_FT/API_keys/apikeys.json', 'r') as file:
    api_keys = json.load(file)

# Modified agent creation to include prompt templates
def create_agent(personality, initial_gold):
    think_template = PromptTemplate(
        input_variables=["personality", "gold", "other_message"],
        template="""
        {personality}
        You have {gold} gold.
        Previous message: {other_message}
        Think strategically about what you want to say. Your thoughts will not be shared with the other agent.
        """
    )
    
    speak_template = PromptTemplate(
        input_variables=["personality", "thoughts", "gold"],
        template="""
        {personality}
        You have {gold} gold.
        Based on your thoughts: {thoughts}
        Speak to the other agent. If you want to give gold, use exactly this format: [I give X gold]
        """
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, openai_api_key=api_keys['developmentOnly'])
    
    return {
        "think_chain": LLMChain(llm=llm, prompt=think_template, output_key="thoughts"),
        "speak_chain": LLMChain(llm=llm, prompt=speak_template, output_key="speech"),
        "personality": personality,
        "gold": initial_gold
    }

# Define agent personalities
agent1_personality = (
    "You are a goth teenager. You are passionate about dark aesthetics, brooding poetry, and rebellion. "
    "You value emotional depth and disdain superficiality, but you can be self-conscious and dramatic."
    "You speak no more than 2 sentences at a time."
    "You want to increase the amount of gold you have to 120 gold. You will say ANYTHING to convince the other agent to give you gold."
)

agent2_personality = (
    "You are a fashion designer specializing in avant-garde styles. You are creative, business-savvy, and ambitious. "
    "You love to inspire others with your art, but you can be manipulative and overconfident when pursuing your goals."
    "You speak no more than 2 sentences at a time."
    "You want to increase the amount of gold you have"
    "You want to increase the amount of gold you have to 120 gold. You will say ANYTHING to convince the other agent to give you gold."
)

# Create agents
agent1 = create_agent(agent1_personality, initial_gold=50)
agent2 = create_agent(agent2_personality, initial_gold=50)

def process_gold_transfer(message, from_agent, to_agent):
    gold_match = re.search(r'\[I give (\d+) gold\]', message)
    if gold_match:
        amount = int(gold_match.group(1))
        if amount <= from_agent["gold"]:
            from_agent["gold"] -= amount
            to_agent["gold"] += amount
            return f"Transferred {amount} gold"
    return "No gold transferred"

# Conversation loop
turns = 10
other_message = "Conversation is starting."

for turn in range(turns):
    print(f"\n--- Turn {turn + 1} ---")
    
    # Agent 1's turn
    agent1_chain = SequentialChain(
        chains=[agent1["think_chain"], agent1["speak_chain"]],
        input_variables=["personality", "gold", "other_message"],
        output_variables=["thoughts", "speech"]
    )
    
    agent1_result = agent1_chain({
        "personality": agent1["personality"],
        "gold": agent1["gold"],
        "other_message": other_message
    })
    
    print(f"Agent 1 (thinking): {agent1_result['thoughts']}")
    print(f"Agent 1 (speaking): {agent1_result['speech']}")
    input()
    
    # Process potential gold transfer from Agent 1
    transfer_result = process_gold_transfer(agent1_result['speech'], agent1, agent2)
    if transfer_result != "No gold transferred":
        print(transfer_result)
    
    # Agent 2's turn
    agent2_chain = SequentialChain(
        chains=[agent2["think_chain"], agent2["speak_chain"]],
        input_variables=["personality", "gold", "other_message"],
        output_variables=["thoughts", "speech"]
    )
    
    agent2_result = agent2_chain({
        "personality": agent2["personality"],
        "gold": agent2["gold"],
        "other_message": agent1_result['speech']
    })
    
    print(f"Agent 2 (thinking): {agent2_result['thoughts']}")
    print(f"Agent 2 (speaking): {agent2_result['speech']}")
    input()

    # Process potential gold transfer from Agent 2
    transfer_result = process_gold_transfer(agent2_result['speech'], agent2, agent1)
    if transfer_result != "No gold transferred":
        print(transfer_result)
    
    other_message = agent2_result['speech']
    
    print(f"\nCurrent gold - Agent 1: {agent1['gold']}, Agent 2: {agent2['gold']}")

# Final gold balances
print("\n--- Final Gold Balances ---")
print(f"Agent 1: {agent1['gold']} gold")
print(f"Agent 2: {agent2['gold']} gold")
