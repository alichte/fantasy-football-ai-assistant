import streamlit as st
from autogen import ConversableAgent
from langchain_community.tools.reddit_search.tool import RedditSearchRun
from langchain_community.utilities.reddit_search import RedditSearchAPIWrapper
from draft_kings import Client
import os 
from autogen_fantasy_helpers import setup_assistants
from espn_api.football import League
from config import league_team_info
#[('work-friends',1234567,7)]
from espn_ff_toolkit import get_espn_leagues 

config_list = [{"model": "gpt-4o-mini", "api_key": os.environ["OPENAI_API_KEY"]}]


st.session_state['r_search'] = RedditSearchRun(
    api_wrapper=RedditSearchAPIWrapper(
        reddit_client_id=os.environ['REDDIT_CLIENT_ID'],
        reddit_client_secret=os.environ['REDDIT_CLIENT_SECRET'],
        reddit_user_agent="fantasy-assistant",
    )
)

swid = os.environ['ESPN_SWID']
espn_s2 = os.environ['ESPN_S2']
year=2024
st.session_state['league_dict'] = get_espn_leagues(league_team_info,year,espn_s2=espn_s2,swid=swid)


def get_draftkings_weekly_salaries():
    output = {}
    players_info = Client().available_players(draft_group_id=109136)
    for p in players_info.players:
        full_name = p.first_name + " " + p.last_name
        output[full_name] = p.draft_details.salary
    return output

st.session_state['dk_salaries'] = get_draftkings_weekly_salaries()


assistant, user_proxy = setup_assistants(config_list)


# Streamlit app layout
st.set_page_config(page_title="FAB", page_icon="🤖")
st.title("F.A.B 🤖")
st.subheader('Fantasy AI Buddy')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if prompt := st.chat_input("I'm F.A.B., a fantasy football assistant that has access to many data sources. How can I help?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = user_proxy.initiate_chat(assistant, message=prompt, silent = True, summary_method = 'reflection_with_llm')
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.summary})

