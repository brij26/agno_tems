from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team import Team
from dotenv import load_dotenv
from project_1.news_agent import news_agent
from project_1.web_search_agent import web_search_agent


load_dotenv()

llm = OpenAIChat(id="gpt-4o-mini")


# form the team
travel_agent = Team(
    members=[news_agent, web_search_agent],
    model=llm,
    id="Travel_agent",
    name="Travel_agent",
    role="You are a team leader and you delegate task to members",
    instructions=["You are an expert travel agent",
                  "Your team can get latest news and places of interest for a particular destination",
                  "Your task is to present the output using proper headlines"],
    stream=True,
    markdown=True
)

travel_agent.cli_app(stream=True, markdown=True)
