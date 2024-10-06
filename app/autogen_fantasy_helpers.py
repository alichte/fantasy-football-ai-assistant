from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
from langchain_community.tools.reddit_search.tool import RedditSearchSchema
from autogen import register_function
from autogen import ConversableAgent
import streamlit as st
from datetime import datetime
import os 
from espn_ff_toolkit import get_rosters, get_free_agents, get_roster_and_projections
from autogen.agentchat.contrib.capabilities.text_compressors import LLMLingua
from autogen.agentchat.contrib.capabilities.transforms import TextMessageCompressor
from autogen.agentchat.contrib.capabilities import transform_messages


def check_reddit(player: str, player_team_subreddit: str) -> str:
    "Check Reddit for any recent player news. Inputs are the player and the subreddit for that player's team"
    search_params = RedditSearchSchema(
        query=player, sort="new", time_filter="week", subreddit="fantasyfootball", limit="5"
        )

    try:
        r_search = st.session_state['r_search']
    except:
        print('Reddit Search information not available in session state')
        return
    
    result = r_search.run(tool_input=search_params.dict())

    try:
        search_params = RedditSearchSchema(
            query=player, sort="new", time_filter="week", subreddit=player_team_subreddit, limit="5"
            )
        extra_result = r_search.run(tool_input=search_params.dict())
        result += extra_result
    except:
        pass
    return result

def google_it(query: str) -> str:
    "Search Google for keywords"
    #this is going to assume you have your environment variables set for GOOGLE_API and GOOGLE_CSE
    search = GoogleSearchAPIWrapper()

    google_search = Tool(
        name="google_search",
        description="Search Google for recent results.",
        func=search.run)
    
    return google_search({'query': query})

def get_rosters_tool()-> str:
    "Get the rosters for all current leagues"
    return get_rosters(st.session_state['league_dict'])

def get_free_agents_tool() -> str:
    "Get the current free agents in all leagues"
    return get_free_agents(st.session_state['league_dict'])

def get_roster_and_projections_tool() -> str:
    "Get the rosters for all current leagues and also all projected and past stats. Higher projectsion means the player is projected to do better by ESPN."
    return get_roster_and_projections(st.session_state['league_dict'])


def get_current_date() -> str:
    "Get the current date, because it is not October 2023"
    current_date = datetime.now()
    return str(current_date)


def check_draftkings_salary(player: str) -> str:
    "Check a player's salary on DraftKings. A higher salary means they are projected to do better by Vegas."
    try:
        salary = st.session_state['dk_salaries'][player]
        return(player, "salary on DraftKings is: ", salary)
    except:
        return(player, "has no salary on DraftKings this week")




def setup_assistants(config_list):
    
    #Creating the actual assistant and giving system instructions
    assistant = ConversableAgent(
        name="Assistant",
        system_message="""You are a helpful AI assistant that is an expert in tool use and in fantasy football. It is long past October of 2023, you need to check the current date to search for current news.
            Think step-by-step about the steps needed to answer an input query, and use the tools available to you to get the information needed at each step.
            Before you recommend adding or dropping any player, be very thorough and check all tools available to you to get the most up to date information possible regarding that player.
            Return 'TERMINATE' when the task is done.""",
        llm_config={"config_list": config_list},
        )

    # The user proxy agent is used for interacting with the assistant agent
    # and executes tool calls.
    user_proxy = ConversableAgent(
        name="User",
        llm_config=False,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        human_input_mode="NEVER",
    )

    llm_lingua = LLMLingua()
    text_compressor = TextMessageCompressor(text_compressor=llm_lingua)
    context_handling = transform_messages.TransformMessages(transforms=[text_compressor])
    context_handling.add_to_agent(assistant)

    register_function(
        google_it,
        caller=assistant,  # The assistant agent can suggest calls to the calculator.
        executor=user_proxy,  # The user proxy agent can execute the calculator calls.
        name="google_it",  # By default, the function name is used as the tool name.
        description="Searches google for recent results using the input as keywords",  # A description of the tool.
    )

    register_function(
        check_reddit,
        caller=assistant,  # The assistant agent can suggest calls to the calculator.
        executor=user_proxy,  # The user proxy agent can execute the calculator calls.
        name="check_reddit",  # By default, the function name is used as the tool name.
        description="Check Reddit for any recent player news. Inputs are the player and the subreddit for that player's team",  # A description of the tool.
    )

    register_function(
        get_roster_and_projections_tool,
        caller=assistant,  # The assistant agent can suggest calls to the calculator.
        executor=user_proxy,  # The user proxy agent can execute the calculator calls.
        description = "Get the rosters for all current leagues and also all projected and past stats"
    )

    register_function(
        get_free_agents_tool,
        caller=assistant,  # The assistant agent can suggest calls to the calculator.
        executor=user_proxy,  # The user proxy agent can execute the calculator calls.
        description = "Get the current free agents in all leagues"
    )

    register_function(
        get_rosters_tool,
        caller=assistant,  # The assistant agent can suggest calls to the calculator.
        executor=user_proxy,  # The user proxy agent can execute the calculator calls.
        description = "Get the rosters for all current leagues"
    )

    register_function(
        get_current_date,
        caller=assistant,  # The assistant agent can suggest calls to the calculator.
        executor=user_proxy,  # The user proxy agent can execute the calculator calls.
        description="Find out what the current date is",  # A description of the tool.
    )

    register_function(
        check_draftkings_salary,
        caller=assistant,  # The assistant agent can suggest calls to the calculator.
        executor=user_proxy,  # The user proxy agent can execute the calculator calls.
        description="Check a player's salary on DraftKings. A higher salary means they are projected to do better",  # A description of the tool.
    )

    return assistant, user_proxy



