def fetch_prompts_chatopenai(llm_response):
    with open('./logs.txt', 'r') as f:
        text = f.read()

    first_prompt_start_index = text.find("""DEBUG:openai:api_version=None data='{"messages": """)
    first_prompt_end_index = text.find(', "model":') + len(', "model":')
    first_prompt = text[first_prompt_start_index : first_prompt_end_index]
    first_prompt_text = first_prompt[first_prompt.find('{"messages": ') + len('{"messages": '): first_prompt.find(', "model":')]

    second_prompt_start_index = text.find("""DEBUG:openai:api_version=None data='{"messages": """, first_prompt_end_index)
    second_prompt_end_index = second_prompt_start_index + text.find(', "model":', second_prompt_start_index)
    second_prompt = text[second_prompt_start_index:  second_prompt_end_index]
    second_prompt_text = second_prompt[second_prompt.find('{"messages": ') + len('{"messages": '): second_prompt.find(', "model":')]
    

    script_result_start_index = second_prompt_text.find('{"role": "function", "content": ') + len('{"role": "function", "content": ')
    script_result_end_index = second_prompt_text.find('", "name": "python_repl_ast"', script_result_start_index)
    script_result_text = second_prompt_text[script_result_start_index + 1: script_result_end_index]

    return {
        'user_input': llm_response['input'],
        'script_generation_prompt': first_prompt_text,
        'script_generation_response': llm_response['intermediate_steps'][0][0] if len(llm_response['intermediate_steps']) > 0 else llm_response['output'],
        'information_retrieval': {
            'python_script': llm_response['intermediate_steps'][0][0].tool_input if len(llm_response['intermediate_steps']) > 0 else '',
            'script_result': script_result_text
            },
        'llm_prompt': second_prompt_text,
        'response': llm_response['output']
    }
