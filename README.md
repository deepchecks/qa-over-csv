# CSV Question Answering

<img src="./assets/deepchecks_llm_app.svg">

🤖 Integrate your Agent-based LLM application with Deepchecks LLM Evaluation using Deepchecks LLM SDK 🤖

- [App description](#app-description)
- [Environment Setup](#environment-setup)
- [How to use Deepchecks LLM SDK?](#how-to-use-deepchecks-llm-sdk)
  - [Instantiate Deepchecks LLM SDK client](#instantiate-deepchecks-llm-sdk-client)
  - [Process the user queries in real time](#process-the-user-queries-in-real-time)
- [Deploy the app to Streamlit](#deploy-the-app-to-streamlit)


## Environment Setup

The application works on Windows, Linux, and Mac. In order to set up your environment, you can create a virtual environment and install all requirements:

```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then rename the `.env.example` file to `.env` and update the following keys as follows:

```python
# Get the OpenAI API key
OPENAI_API_KEY='<OPENAI_API_KEY>'
# Login to deepchecks' service and generate new API Key (Configuration -> API Key) and place it here
DEEPCHECKS_LLM_API_KEY='<DEEPCHECKS_LLM_API_KEY>'
# Fill deepchecks host name here
DEEPCHECKS_LLM_HOST_URL='<DEEPCHECKS_LLM_HOST_URL>'
```

Now, you are ready to start the streamlit app locally by running the following command:
```python
streamlit run main.py
```

After running the application, if your Deepchecks LLM application name and version name does not match with the names on the Deepchecks LLM app, you need to update the Deepchecks LLM application name and version name from the UI by going to the **Settings** section as shown in the below image:

<img src="./assets/settings-section.png">

You can also update the GPT model from the **Settings** section. By default, the GPT model is selected to *"gpt-3.5-turbo"*.
# App description
This application utilizes [Langchain's Notion Question-Answering Language Model (LLM)](https://github.com/hwchase17/notion-qa), which has been trained on documents from a company named Blendle. This demo application will help you understand how Deepchecks LLM SDK traces OpenAI requests and stores the required information in Deepchecks LLM web application. We have used the `RetrievalQAWithSourcesChain` from `langchain` which helps to send the user query to our LLM (in this case, its OpenAI) and then provide us with a response and the source of the response. To find the relevant documents from Notion based on the user input, we use `faiss` indexing based strategy. The LLM can answer most of the HR related questions an employee may ask. Some of the examples of user questions and their response are shown below:

> **User Input:** Where is the company located?<br>
  **LLM Response:** The company is located in Utrecht, Netherlands.

> **User Input:** Process for claiming telephone reimbursement?<br>
  **LLM Response:** To claim telephone reimbursement, employees need to log in to their NMBRS account and click on "Expenses Declaration" to submit their claim. The claim will be forwarded to finance and paid out together with the next salary. Employees can also use the NMBRS app to submit their claim. The reimbursement is provided on a monthly basis along with the paycheck. Any employee of Blendle with a contract is eligible for reimbursement, regardless of the number of hours or the type of contract. The process for claiming reimbursement for travel expenses is to take a picture of the receipt, add the expense and receipt to Nmbrs (salarisbalie), have it approved by the manager, and get paid back in the monthly payroll run. For specific questions, employees can contact finance@blendle.com.


# How to use Deepchecks LLM SDK?
Before proceeding, make sure that you have an app created in the Deepchecks LLM evaluation application. We will not use the auto collect feature of the SDK here since there can be multiple LLM calls depending upon your agent pipeline. So we will be using the logging each interaction using the `log_interaction()` function provided by the SDK.

## Instantiate Deepchecks LLM SDK client

```python
from deepchecks_llm_client.client import dc_client

dc_client.init(host=DEEPCHECKS_LLM_HOST_URL,
               api_token=DEEPCHECKS_LLM_API_KEY,
               app_name=DEEPCHECKS_LLM_APP_NAME,
               version_name=DEEPCHECKS_LLM_APP_VERSION_NAME,
               env_type=EnvType.PROD,
               auto_collect=False  # Setting auto collect to False
               )
```

## Process the user queries in real time

```python

result = call_llm_with_chatopenai(st.session_state.dataset, user_input)

dc_client.log_interaction(user_input=result['user_input'],
                          model_response=result['response'],
                          full_prompt=result['llm_prompt'],
                          information_retrieval=str(result['information_retrieval']),
                          ext_interaction_id=user_generated_unique_key)

```

## Annotate the LLM response

```python
from deepchecks_llm_client.api import AnnotationType

# If you want to annotate the LLM response as 'Good'
dc_client.annotate(ext_interaction_id=user_generated_unique_key, annotation=AnnotationType.GOOD)

# If you want to annotate the LLM response as 'Bad'
dc_client.annotate(ext_interaction_id=user_generated_unique_key, annotation=AnnotationType.GOOD)
```

# Deploy the app to Streamlit
The code to run the StreamLit app is in `main.py`. Note that when setting up your StreamLit app you should make sure to add all the environment variables in your `.env` file as a secret environment variable as Secrets in Settings of your deployed Streamlit app.
