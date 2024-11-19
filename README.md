"""
LLM Agent for Meeting Workflow Automation

An Autonomous agent created using Langchain and langchain agents to create project proposals and automate meeting workflow.

Read the blog: https://www.ionio.ai/blog/lets-automate-your-meeting-workflow-with-langchain-and-agents-code-included

Sneak Peek:
- A visual demonstration of the product is available at: 
  https://assets-global.website-files.com/62528d398a42420e66390ef9/65dcad8e72447b6c41891851_product_demo.gif

How it Works:
1. Get information about prospect and idea:
   - The agent retrieves information about a prospect & their idea from the internet using the Perplexity API when a call is booked.

2. Find possible solution:
   - It finds possible solutions for the idea and how to convert that idea into an actual product from the internet.

3. Create proposal:
   - Creates a professional project proposal from the given idea, client information, and solution, which includes other information like tech stack, timeline, project link, etc.

4. Convert proposal to sharable document:
   - Saves the project proposal as a Notion document or Word document.

Architecture:
- A visual representation of the architecture is available at:
  https://assets-global.website-files.com/62528d398a42420e66390ef9/65dcab8b7d7f1710c7221f84_image4.png

Getting Started:

Prerequisites:
- Python and Anaconda installed on your machine
- OpenAI API key
- Perplexity API key
- Notion API key

How to Run:
1. Clone the repository.
2. Create a file called `constants.py` in the same folder and store all of your API keys like this:

   OPENAI_API_KEY = <key_here>
   PERPLEXITY_API_KEY = <key_here>
   NOTION_API_KEY = <key_here>

3. Open any Jupyter notebook from the repository.
4. Select your existing Python environment or create one using Anaconda.
5. Run the code.
"""