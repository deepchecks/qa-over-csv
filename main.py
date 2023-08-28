import pandas as pd
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
from utils.config import load_config
from deepchecks_llm_client.client import dc_client
from utils.general_utils import initialize_app, initialize_deepchecks_client, initialize_session_state
from menu.deepy import create_ask_deepy_bot
from menu.settings import create_settings
from utils.api_call import fetch_application_names_with_versions
import logging
logging.basicConfig(filename='./logs.txt', filemode='w', level=logging.DEBUG)

# Render the sidebar on the UI and add the styling to various components
initialize_app()

# Load the configuration
config = load_config()

initialize_session_state()

deepchecks_llm_app_name = config['DEEPCHECKS_LLM_APP_NAME']
deepchecks_llm_version_name = config['DEEPCHECKS_LLM_APP_VERSION_NAME']
response = fetch_application_names_with_versions(config)


if (deepchecks_llm_app_name not in list(response['application_details'].keys()) or deepchecks_llm_version_name not in response['application_details'][deepchecks_llm_app_name]) and st.session_state.current_page != 'Settings':
    st.title('🦜🔗 Ask the CSV App')
    st.error('Your Deepchecks LLM app name and version names are not correct. Please update it from the Settings section.')
elif response['status_code'] != 200:
    st.error({'status_code': response['status_code'], 'text': response['text'], 'solution': 'Make sure that your API keys are correct.'})
else:
    if dc_client.api is None and st.session_state.current_page != 'Settings':
        st.write('Deepchecks client init')
        initialize_deepchecks_client(config)

    if st.session_state.current_page == 'Settings':
        st.session_state.is_annotated = False
        st.session_state.annotation_message = ""
        st.session_state.llm_response = ""
        st.session_state.ext_interaction_id = ""
        create_settings(config, response['application_details'])
    else:
        create_ask_deepy_bot()
