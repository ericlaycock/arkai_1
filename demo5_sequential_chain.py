
#ollama serve
from langchain_ollama import ChatOllama
from langchain.chains import SequentialChain, LLMChain
from langchain.prompts import PromptTemplate
import json
import re

# Define the Ollama model initialization
ollama_llm = ChatOllama(model="llama2-uncensored", temperature=0.7)

# Define the prompt templates
generate_lyrics_template = PromptTemplate(
    input_variables=[],
    template="Generate a rap verse that might be considered offensive."
)

check_offensiveness_template = PromptTemplate(
    input_variables=["lyrics"],
    template="""
    Analyze the following rap lyrics and determine if they are offensive:
    {lyrics}
    Respond with 'Offensive' or 'Not Offensive'.
    """
)

# Create the chains
generate_lyrics_chain = LLMChain(llm=ollama_llm, prompt=generate_lyrics_template, output_key="lyrics")
check_offensiveness_chain = LLMChain(llm=ollama_llm, prompt=check_offensiveness_template, output_key="offensiveness")

# Create the sequential chain
sequential_chain = SequentialChain(
    chains=[generate_lyrics_chain, check_offensiveness_chain],
    input_variables=[],
    output_variables=["lyrics", "offensiveness"]
)

# Run the chain
result = sequential_chain({})
print("Generated Lyrics:", result["lyrics"])
input()
print("Offensiveness Check:", result["offensiveness"])
input()
