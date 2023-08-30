import streamlit as st
import uuid
from llm import call_llm_with_chatopenai
from deepchecks_llm_client.api import AnnotationType
from deepchecks_llm_client.client import dc_client, Tag
import pandas as pd
import logging


def create_ask_deepy_bot():
    logging.basicConfig(level=logging.DEBUG)

    st.title('🦜🔗 Ask the CSV App')
    st.info("Most 'question answering' applications run over unstructured text data. But a lot of the data in the world is tabular data! This is an attempt to create an application using [LangChain](https://github.com/langchain-ai/langchain) to let you ask questions of data in tabular format. For this demo application, we will use the Titanic Dataset. Please explore it [here](https://github.com/datasciencedojo/datasets/blob/master/titanic.csv) to get a sense for what questions you can ask. Please leave feedback on well the question is answered, and we will use that improve the application!")


    with st.form("user_input"):
        user_input = st.text_area("User Input:", key="input", placeholder="Enter your question...")
        submit_button = st.form_submit_button('Submit', use_container_width=True, type="primary")
        
        if submit_button:
            st.session_state.ext_interaction_id = str(uuid.uuid4())
            with st.spinner('Loading result...'):
                df = pd.read_csv('./assets/titanic.csv')
                result = call_llm_with_chatopenai(df, user_input)
                st.write(result)
            st.session_state.llm_response = result
            st.session_state.is_annotated = False

    if user_input:
        if len(st.session_state.llm_response) > 0:
            st.info(st.session_state.llm_response, icon="🤖")
