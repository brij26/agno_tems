from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv

# load all keys to env
load_dotenv()

# define one model
llm = OpenAIChat(id="gpt-4o-mini")

# define tool
news_tool = DuckDuckGoTools()

# define agent
news_agent = Agent(
    id="news_agent",
    name="news agent",
    model=llm,
    tools=[news_tool],
    instructions=["You are expert in new search",
                  "You have one tool to search new for particulat destination",
                  "your task is to search top five news headlines for particular destination and give a summary of it"]
)
