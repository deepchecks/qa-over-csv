import streamlit as st
import uuid
from llm import call_llm_with_chatopenai
from deepchecks_llm_client.api import AnnotationType
from deepchecks_llm_client.client import dc_client, Tag
import pandas as pd
import logging


def create_ask_deepy_bot():
    logging.basicConfig(level=logging.DEBUG)

    st.title('🦜🔗 Deepy Bot')
    st.info("Upload any CSV or Excel file containing your dataset and ask questions to it!!")

    upload_file = st.file_uploader("Upload dataset", type=['csv','xls','xlsx'])
    if upload_file is not None:
        with st.spinner('Uploading dataset...'):
            dataframe = pd.read_csv(upload_file, encoding='latin-1') if upload_file.type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' else pd.read_excel(upload_file)
            st.session_state.dataset = dataframe

    if len(st.session_state.dataset) > 0:
        with st.form("user_input"):
            user_input = st.text_area("User Input:", key="input", placeholder="Enter your question...")
            submit_button = st.form_submit_button('Submit', use_container_width=True, type="primary")
            
            if submit_button:
                with st.spinner('Loading result...'):
                    result = call_llm_with_chatopenai(st.session_state.dataset, user_input)
                    st.session_state.ext_interaction_id = str(uuid.uuid4())
                    # dc_client.set_tags({Tag.USER_ID: "user@deepchecks.com"})  - Removed so there will be no "Raw Data" in samples page
                    dc_client.log_interaction(user_input=result['user_input'],
                                              model_response=result['response'],
                                              full_prompt=result['llm_prompt'],
                                              information_retrieval=str(result['information_retrieval']),
                                              ext_interaction_id=st.session_state.ext_interaction_id)
                    dc_client.set_tags({})
                st.session_state.llm_response = result['response']
                st.session_state.is_annotated = False

        if user_input:
            if len(st.session_state.llm_response) > 0:
                st.info(st.session_state.llm_response, icon="🤖")
            if not st.session_state.is_annotated:
                placeholder_column = st.empty()
                columns = placeholder_column.columns(2)
                with columns[0]:
                    placeholder_good = st.empty()
                    good = placeholder_good.button('👍 Good', key='good_btn', use_container_width=True)

                with columns[1]:
                    placeholder_bad = st.empty()
                    bad = placeholder_bad.button('👎 Bad', key='bad_btn', use_container_width=True)

                if good or bad:
                    st.session_state.is_annotated = True
                    placeholder_good.empty()
                    placeholder_column.empty()
                    placeholder_bad.empty()
                if good:
                    st.session_state.annotation_message = "Good"
                    dc_client.annotate(ext_interaction_id=st.session_state.ext_interaction_id, annotation=AnnotationType.GOOD)
                elif bad:
                    st.session_state.annotation_message =  "Bad"            
                    dc_client.annotate(ext_interaction_id=st.session_state.ext_interaction_id, annotation=AnnotationType.BAD)

                if not submit_button and st.session_state.is_annotated:
                    if 'Bad' in st.session_state.annotation_message:
                        st.button('👎 Bad', use_container_width=True)
                        if st.session_state.is_annotated:
                            st.markdown("""<style>
                                            [data-testid=stVerticalBlock]>div>div>button,
                                            [data-testid=stVerticalBlock]>div>div>button:hover,
                                            [data-testid=stVerticalBlock]>div>div>button:active,
                                            [data-testid=stVerticalBlock]>div>div>button:focus:not(:active) {
                                                background-color: #FC636B;
                                                border: 1px solid #FC636B;
                                                pointer-events: none;
                                                color: white;
                                            }
                                    </style>""", unsafe_allow_html=True)

                    else:
                        st.button('👍 Good', use_container_width=True)
                        if st.session_state.is_annotated:
                            st.markdown("""<style>
                                            [data-testid=stVerticalBlock]>div>div>button,
                                            [data-testid=stVerticalBlock]>div>div>button:hover,
                                            [data-testid=stVerticalBlock]>div>div>button:active,
                                            [data-testid=stVerticalBlock]>div>div>button:focus:not(:active) {
                                                background-color: #37A862;
                                                border: 1px solid #37A862;
                                                color: white;
                                                pointer-events: none;
                                            }
                                            </style>""", unsafe_allow_html=True)
