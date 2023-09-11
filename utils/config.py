from dotenv import dotenv_values
import os
import streamlit as st
from configparser import ConfigParser 

def load_config():
    """Load all the required credentials from the .env file or streamlit cloud.

    Returns
    -------
    OrderDict containing all the variables from the .env file.
    """
    if os.path.exists('.env'):
        config = dotenv_values(".env")
        os.environ['OPENAI_API_KEY'] = config["OPENAI_API_KEY"]
    else:
        config = {}
        config['DEEPCHECKS_LLM_API_KEY'] = st.secrets['DEEPCHECKS_LLM_API_KEY']
        config['DEEPCHECKS_LLM_HOST_URL'] = st.secrets['DEEPCHECKS_LLM_HOST_URL']

    cp = ConfigParser()
    cp.read('./config.ini')
    config['DEEPCHECKS_LLM_APP_NAME'] = cp.get('DEEPCHECKS_LLM_APP', 'DEEPCHECKS_LLM_APP_NAME')
    config['DEEPCHECKS_LLM_APP_VERSION_NAME'] = cp.get('DEEPCHECKS_LLM_APP','DEEPCHECKS_LLM_APP_VERSION_NAME')
    config['GPT_MODEL'] = cp.get('DEEPCHECKS_LLM_APP','GPT_MODEL')

    return config

def update_config(app_name, app_version, gpt_model):
    # Write the updated environment variables to the .env file
    cp = ConfigParser()
    cp.read('./config.ini')
    cp.set('DEEPCHECKS_LLM_APP', 'DEEPCHECKS_LLM_APP_NAME', app_name)
    cp.set('DEEPCHECKS_LLM_APP', 'DEEPCHECKS_LLM_APP_VERSION_NAME', app_version)
    cp.set('DEEPCHECKS_LLM_APP', 'GPT_MODEL', gpt_model)

    with open('config.ini', 'w') as configfile:
        cp.write(configfile)
