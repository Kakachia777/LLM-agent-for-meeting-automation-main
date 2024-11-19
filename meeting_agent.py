# Meeting Automation LLM Agent
# This script creates an agent to automate meeting workflows, including gathering information, finding solutions, and creating project proposals.

import os
import json
import requests
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.tools import BaseTool
from langchain.agents import initialize_agent
from notion_client import Client
from openai import OpenAI
import pypandoc

# Constants
import constants  # Ensure you have a constants.py file with your API keys

# Initialize LLM
OPENAI_API_KEY = constants.OPENAI_API_KEY
llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    temperature=0.6,
    model_name='gpt-4'
)

# Initialize conversational memory
conversational_memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True
)

# Define tools
class GetClientDetails(BaseTool):
    name = "Client details extractor"
    description = "Use this tool when you have a platform name, idea, or platform link and want to find more information about the CEO and proposed idea."

    def _run(self, website):
        url = "https://api.perplexity.ai/chat/completions"
        payload = {
            "model": "pplx-70b-online",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an artificial intelligence agent that extracts information by searching online."
                        "Return information in this format if it exists:"
                        "Title of website or platform: "
                        "Proposed idea:"
                        "CEO Information:"
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "I am giving you a platform name, idea, or platform link. Find the latest information about"
                        "the platform by visiting the given link and return at least 200 words description about the idea and"
                        "at least 150 words description about the CEO, their goal, and achievements."
                        "Please make it as detailed as possible and always refer to online information."
                        f"Here is the platform link or name: {str(website)}"
                    )
                },
            ]
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {constants.PERPLEXITY_API_KEY}"
        }
        response = requests.post(url, json=payload, headers=headers)
        return response

    def _arun(self, website):
        raise NotImplementedError("This tool does not support async")

class GetPlatformInfo(BaseTool):
    name = "Platform info extractor"
    description = "Use this tool when you have a description about a meeting and need to find the proposed idea, client name, or platform link."

    def _run(self, description):
        url = "https://api.perplexity.ai/chat/completions"
        payload = {
            "model": "pplx-70b-online",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You have a description of a meeting and need to find the proposed idea, client name, and website link."
                        "Use the client info extractor tool to get more information."
                        "Return it in this format:"
                        "Idea: <idea>"
                        "Client Info: <client_info>"
                        "Platform Link: <platform_link>"
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "If anything is not provided in the description, use the internet and Google search to find the actual information."
                        f"Here is the meeting description: {str(description)}"
                    )
                },
            ]
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {constants.PERPLEXITY_API_KEY}"
        }
        response = requests.post(url, json=payload, headers=headers)
        return response

    def _arun(self, website):
        raise NotImplementedError("This tool does not support async")

class GetIdeaSolution(BaseTool):
    name = "Solution extractor"
    description = "Use this tool when you have an idea description and client information to find solutions on how to achieve the given idea."

    def _run(self, description):
        url = "https://api.perplexity.ai/chat/completions"
        payload = {
            "model": "pplx-70b-online",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You have an idea description and need to find around 3-4 solutions to achieve the given idea using AI-ML"
                        "or web development technologies. Search online about tech stack, resources, timeline of the project, and YouTube videos."
                        "Send it with proper formatting and line breaks in this format:"
                        "Solution: <solution>"
                        "Tech stack: <tech_stack>"
                        "Timeline: <timeline>"
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Here is the idea description: {str(description)}"
                    )
                },
            ]
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {constants.PERPLEXITY_API_KEY}"
        }
        response = requests.post(url, json=payload, headers=headers)
        return response

    def _arun(self, website):
        raise NotImplementedError("This tool does not support async")

# Initialize agent
tools = [GetClientDetails(), GetPlatformInfo(), GetIdeaSolution()]
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True,
    max_iterations=3,
    early_stopping_method='generate',
    memory=conversational_memory,
    handle_parsing_errors=True
)

# Test the agent
para = agent(
    "First find the idea, client name, and platform link using the Platform info extractor tool and find 150 words information about the proposed idea about the product, goals, and achievements of the CEO. Once you got the information about their idea, then find how we can help them to build it in 200 words."
    "Fetch real-time data from the internet every time."
    "This information is going to be added in the project proposal, so please write in detail, and sections like CEO_Info, idea, and solution must be explained in 600 words each."
    "Return your response in Python dict format like below and please use proper line breaks: "
    """
    "platform_name": platform_name
    "CEO_Name": ceo_name
    "idea": idea
    "solution": solution
    "tech_stack": tech stack
    "timeline": timeline
    "Platform_link": platform_link
    """
    "Here is the description:"
    "Hey there, myself Rohan, and we are hosting this meeting to discuss my idea of making a Twitter automation tool with several features like automated tweets, scheduled tweets, tweet improvement guides, etc."
)
output = json.loads(para["output"])
print(output)

# Format details for Notion
client = OpenAI(api_key=constants.OPENAI_API_KEY)
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"""
                I am giving you some data in Python dict format, and you will have to add more information by searching about it online in the given data so that it can be added in a project proposal, but don't add any fake information. Once you got the information, then return the data in the same format.
                Try to add more information by yourself too to make it more detailed and make it around 1000 words. Don't return anything except this dictionary and also please use proper line breaks in every paragraph of each section of the dict.
                Here is the information about fields in the given dict: 
                platform_name: Name of platform
                CEO_Info: Background about CEO and information about CEO
                CEO_Name: Name of CEO
                idea: project idea
                solution: solution on how we can solve the given problem statement and how to achieve the given idea
                tech_stack: tech stack used to build the solution
                timeline: timeline for the project
                Platform_link: link to the platform
                Here is the data: 
                {para["output"]}
            """,
        }
    ],
    model="gpt-4",
    temperature=0.7
)
output = chat_completion.choices[0].message.content
output = json.loads(output)

# Add data to Notion
notion = Client(auth=constants.NOTION_API_KEY)
parent = {"type": "page_id", "page_id": "14ffc7f5-774f-46d6-8653-e6f24dfae758"}
properties = {
    "title": {
        "type": "title",
        "title": [{"type": "text", "text": {"content": f"Meeting with {output['CEO_Name']} about {output['platform_name']}"}}],
    },
}
children = [
    {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "🚀 Platform Name"}}]
        }
    },
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": output['platform_name']}}]
        }
    },
    {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "📝 Idea Description"}}]
        }
    },
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": output['idea']}}]
        }
    },
    {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "💡 How we can help?"}}]
        }
    },
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": output['solution']}}]
        }
    },
    {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"type": "text", "text": {"content": "⚒️ What tech stack we can use?"}}]
        }
    },
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": output['tech_stack']}}]
        }
    },
    {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"type": "text", "text": {"content": "⌛ What is timeline of project?"}}]
        }
    },
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": output['timeline']}}]
        }
    },
    {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"type": "text", "text": {"content": "🤔 Info about CEO"}}]
        }
    },
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": output['CEO_Info']}}]
        }
    },
    {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "🔗 Platform Link"}}]
        }
    },
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": output['Platform_link']}}]
        }
    },
]
create_page_response = notion.pages.create(
    parent=parent, properties=properties, children=children
)
print(create_page_response)

# Create proposal as a Word document
output = pypandoc.convert_text(output, 'docx', format='md', outputfile="output.docx")
print(output) 