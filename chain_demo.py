# Chains in Langchain

# In Langchain, a chain is a series or chain of different components that can be connected with each other and can pass input and output to process data.
# These chains are created by one or more LLMs. For example, if you want to generate some data using LLM and then use that output as an input for another LLM, you can create a chain for this purpose.

# We use `SimpleSequentialChain` when we have only one input and single output in a chain.
# For example, we have a cuisine and we want to generate a restaurant name from the given cuisine name and from that name we want to generate 10 dishes to add to the menu.

# As we can see here, one task is dependent on another, and here is where we will create our first chain.

# First, install openai and langchain modules
# !pip install openai langchain  # Uncomment this line to install the packages if not already installed

import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain

# Setup our LLM, we will use GPT-3.5 Turbo model for this tutorial.
# Get your API key from the OpenAI dashboard and add it as an environment variable in your code as it’s recommended to keep it private.
OpenAI_LLM = OpenAI(temperature=0.6, api_key=os.environ["OPENAI_KEY"])

# Here temperature shows the creativity of output, the more temperature is the more creative answer you will get and it's not recommended for any calculation-related output but it's very useful for content writing.

# Now we have LLM setup so let’s try it once
bot = OpenAI_LLM("Say hello if you are working!")
print(bot)

# After running it you will get an output from LLM saying hello and now our LLM is working perfectly!

# So let’s create a chain, but first we will need to create a prompt template for our LLM which we can create using PromptTemplate from langchain

# Create first chain
prompt_1 = PromptTemplate.from_template(
    "Give me a {cuisine} restaurant name. Only return name"
)

# Here cuisine is an input from user and it will be automatically added in our prompt dynamically.
# So now we have our prompt and LLM ready so now we can create chain using LLMChain
first_chain = LLMChain(llm=OpenAI_LLM, prompt=prompt_1)
# To run this chain use below code
# first_chain.run("Indian")  # Passing cuisine parameter

# Now our first chain is ready which will give us restaurant name.
# Now create one more chain which will give us food items list for the given restaurant name.

# Create second chain
prompt_2 = PromptTemplate.from_template(
    "Give me 10 dish names for restaurant {restaurant}"
)
second_chain = LLMChain(llm=OpenAI_LLM, prompt=prompt_2)

# Now let’s combine these 2 chains using SimpleSequentialChain. The order of chains matters in sequential chains.
final_chain = SimpleSequentialChain(chains=[first_chain, second_chain])
response = final_chain.run("Indian")
print(response)

# Once we run this code, we will get the name of 10 dishes based on the given cuisine and restaurant name!

# Creating Sequential chain
# But what if we want both restaurant name and dishes name in output? 🤔

# This is where `SequentialChain` comes into picture, it allows us to have multiple inputs and outputs unlike SimpleSequentialChain. So let’s try it!

# Create first chain
prompt_1 = PromptTemplate.from_template(
    "Give me a {cuisine} restaurant name. Only return name"
)
# Here we will specify output_key which will be used in next chain as an input
first_chain = LLMChain(llm=OpenAI_LLM, prompt=prompt_1, output_key="restaurant_name")

# Create second chain
prompt_2 = PromptTemplate.from_template(
    "Give me 10 dish names for restaurant {restaurant}"
)
second_chain = LLMChain(llm=OpenAI_LLM, prompt=prompt_2, output_key="dishes")

# Combine both chains into sequential chain
final_sequential_chain = SequentialChain(
    input_variables=["cuisine"],
    # We want both restaurant name and result in output
    output_variables=["restaurant_name", "dishes"],
    chains=[first_chain, second_chain]
)
# In sequential chain, we can have multiple inputs so use tuple here for parameters.
final_sequential_chain({"cuisine": "Mexican"})

# After running the code, we will get both restaurant name and dishes list and this is how you can create chains using langchain according to your use cases. 