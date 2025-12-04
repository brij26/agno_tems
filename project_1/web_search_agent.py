from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv

load_dotenv()

llm = OpenAIChat(id="gpt-4o-mini")

web_search_tool = DuckDuckGoTools()

web_search_agent = Agent(
    id="web_search_agent",
    name="web_search_agent",
    model=llm,
    role="Get information for the places to the visit at the destination",
    tools=[web_search_tool],
    instructions=["You are a web search agent",
                  "Your goal is to search for the places of interest for a particular destination"]
)
