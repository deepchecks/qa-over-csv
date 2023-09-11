import streamlit as st
from utils.config import update_config
from utils.general_utils import initialize_deepchecks_client
import time
from deepchecks_llm_client.client import dc_client

GPT_MODELS = ['gpt-3.5-turbo', 'gpt-4']

def create_settings(config, application_details):
    st.header('Settings')
    st.markdown("""Update your Deepchecks LLM application name and version name below:""")
    
    columns = st.columns(3, gap='medium')
    if config['DEEPCHECKS_LLM_APP_NAME'] not in application_details.keys():
        app_names = list(application_details.keys())
    else:
        app_names = [config['DEEPCHECKS_LLM_APP_NAME'], *[key for key in application_details.keys() if key != config['DEEPCHECKS_LLM_APP_NAME']]]

    with columns[0]:
        app_name = st.selectbox('Deepchecks LLM Application Name:', (tuple(app_names)))
        if app_name == config['DEEPCHECKS_LLM_APP_NAME']:
            app_version = [config['DEEPCHECKS_LLM_APP_VERSION_NAME'], *[key for key in application_details[app_name] if key != config['DEEPCHECKS_LLM_APP_VERSION_NAME']]]
        else:
            app_version = application_details[app_name]

    with columns[1]:
        version = st.selectbox('Deepchecks LLM Version Name:', (tuple(app_version)))

    with columns[2]:
        if config['GPT_MODEL'] in GPT_MODELS:
            gpt_models = [config['GPT_MODEL'], *[model for model in GPT_MODELS if model != config['GPT_MODEL']]]
        else:
            gpt_models = GPT_MODELS 
        gpt_model_name = st.selectbox('GPT Model:', (tuple(gpt_models)))

    submit_button = st.button('Update', use_container_width=True)
    if submit_button:
        with st.spinner('Updating the app name and version'):
            update_config(app_name, version, gpt_model_name)
            if dc_client.api is None:
                config['DEEPCHECKS_LLM_APP_NAME'] = app_name
                config['DEEPCHECKS_LLM_APP_VERSION_NAME'] = version
                initialize_deepchecks_client(config)
            else:
                dc_client.app_name(app_name).version_name(version)
            time.sleep(2)
