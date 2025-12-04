from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.team import Team
from dotenv import load_dotenv

load_dotenv()

llm = OpenAIChat(id="gpt-4o-mini")

# create one database
db = SqliteDb(db_file="team_db/demo.db",
              session_table="session_table")

# define the session state
session_state = {"grocery_list": [], "todo_list": [], "study_list": []}

# define the function which can add item to list


def add_item(session_state: dict, list_name: str, item_name: str) -> str:
    """This function can add item to particular list"""
    item_name = item_name.lower()
    list_name = list_name.lower()
    if item_name in session_state[list_name]:
        return f"{item_name} is already in {list_name}"
    else:
        session_state[list_name].append(item_name)
        return f"{item_name} is added to the {list_name}"


def remove_item(session_state: dict, list_name: str, item_name: str) -> str:
    """This function can remove the given item from the list"""
    list_name = list_name.lower()
    item_name = item_name.lower()

    # checking either list have items or not
    if not session_state[list_name]:
        return f"{list_name} is empty. there is no item inside it"
    else:
        session_state[list_name].remove(item_name)
        return f"{item_name} is removed from {list_name} successfully"


def list_item(session_state: dict, list_name: str) -> str:
    """This function can list the items from the given list"""
    list_name = list_name.lower()
    text = "\n".join([f"- {item}" for item in session_state[list_name]])
    return f"the item in {list_name} is {text}"


def clear_list(session_state: dict, list_name: str) -> str:
    """This function can clear the given list"""
    list_name = list_name.lower()
    session_state[list_name].clear()
    return f"list : {list_name} cleared of all items"

# now we will define the agent one by one


#  1.grocery agent
grocery_agent = Agent(
    id="grocery_agent",
    name="Grocery agent",
    model=llm,
    role="Manages list of items in grocery list",
    instructions=["Yor are an expert in managing grocery lists",
                  "You can add or remove items from the list",
                  "You can also see the items in the list",
                  "You can clear the list of items if asked to do so"],
    tools=[add_item, remove_item, list_item, clear_list]
)

# 2. to do agent
TODO_agent = Agent(
    id="TODO_agent",
    name="TODO agent",
    model=llm,
    role="Manages list of items in to do  list",
    instructions=["Yor are an expert in managing to do lists",
                  "You can add or remove items from the list",
                  "You can also see the items in the list",
                  "You can clear the list of items if asked to do so"],
    tools=[add_item, remove_item, list_item, clear_list]
)

# 3. Study agent
study_agent = Agent(
    id="study_agent",
    name="study agent",
    model=llm,
    role="Manages list of items in study list",
    instructions=["Yor are an expert in managing study lists",
                  "You can add or remove items from the list",
                  "You can also see the items in the list",
                  "You can clear the list of items if asked to do so"],
    tools=[add_item, remove_item, list_item, clear_list]
)


# define the team
list_manager = Team(
    members=[grocery_agent, TODO_agent, study_agent],
    name="Personal list manager",
    model=llm,
    db=db,
    role="You are an expert in manages in sub agents with great accuracy",
    instructions=["You are an expert in managing different types of personal list",
                  "the lists are : grocery_list, todo_list, study_list",
                  "The groceries list is : grocery_list",
                  "The TODO list is : todo_list",
                  "The study list is : study_list",
                  "Make sure to use list name as mentioned",
                  "Your task is to manage this three lists where you can add, remove, list down items or clear my specified list",
                  "decide the name of the list based on the user query",
                  "task will be handled by the members, you just delegate what to do"],
    stream=True,
    markdown=True,
    session_state=session_state,
    add_session_state_to_context=True,
    add_history_to_context=True,
    num_history_runs=3
)


list_manager.cli_app(stream=True, markdown=True)
