# Langchain Agents
# Langchain Agents are the digital workhorses within the Langchain ecosystem, bringing the magic of automation to life.
# These agents are essentially intelligent entities, programmed to understand and respond to human language,
# allowing them to perform a myriad of tasks autonomously.

# Let's create a basic agent which can fetch information from the internet.

# First, install openai and langchain modules.
# !pip install openai langchain  # Uncomment this line to install the packages if not already installed

import os
from langchain.llms import OpenAI
from langchain.agents import AgentType, initialize_agent, load_tools

# Setup our LLM, we will use GPT-3.5 Turbo model for this tutorial.
# Get your API key from the OpenAI dashboard and add it as an environment variable in your code
# as it’s recommended to keep it private.
OpenAI_LLM = OpenAI(temperature=0.6, api_key=os.environ["OPENAI_KEY"])

# We will use `serpapi` tool for this scenario with our agent.
# First, get your serpapi key from their website and once you get the API key,
# store it in your environment variable and let’s start building our agent.

# Load the tool using `load_tools` method and provide our OpenAI LLM which we created before.
tools = load_tools(["serpapi"], llm=OpenAI_LLM)

# Initialize our agent with given tools, LLM, and agent type.
agent = initialize_agent(
    tools,
    llm=OpenAI_LLM,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# And once everything is done, now we can finally run our agent by giving it a prompt like this:
result = agent.run("What is the current value of 1 dollar in rupees?")
print(result) 