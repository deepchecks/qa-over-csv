from langchain.agents import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from utils.llm_utils import fetch_prompts_chatopenai

def call_llm_with_chatopenai(df, user_input):
    open("./logs.txt", "w", encoding='utf-8').close()
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    agent_executor_kwargs = { "handle_parsing_errors": True }
    agent = create_pandas_dataframe_agent(llm, df, return_intermediate_steps=True, agent_executor_kwargs=agent_executor_kwargs, 
                        max_iterations=5,agent_type=AgentType.OPENAI_FUNCTIONS, verbose=True)


    response = agent({"input": user_input}, include_run_info=True)
    return fetch_prompts_chatopenai(response)
