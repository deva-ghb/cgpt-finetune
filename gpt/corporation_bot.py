from dotenv import load_dotenv
import openai
import os
load_dotenv()
# set the key
openai.api_key = os.environ.get("OPENAI_API_KEY")
from typing import Any
from elastic.elastic_langchain import query_elastic_search_vector_index
from context.context_chat import get_augmented_prompt, put_turn

INDEX_NAME = 'corporation_index'
def ask_corporation_bot(query : str, user_id : str):
    relevant_page_content = query_elastic_search_vector_index(index= INDEX_NAME,
                                                              query = query,
                                                              k = 2)
    
    
    augmented_prompt = get_augmented_prompt(user_id, query) 
    # messages=[
    #         {"role": "system", "content": relevant_page_content},
    #         {"role": "user", "content": augmented_prompt}
    #     ]

    # response = 'hello always!'

    print('messages = ', str([
            {"role": "system", "content": relevant_page_content},
            {"role": "user", "content": augmented_prompt}
        ]))
   
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": relevant_page_content},
            {"role": "user", "content": augmented_prompt}
        ],
    temperature = 0.2
    )

    print('completion ', completion)

    content = completion["choices"][0]["message"]["content"]

    content = content.replace('"', "")
    content = content.replace("'", "")

    put_turn(user_id= user_id, user_query= query, bot_response = content)

    return {
        'response' : content
    }
    # print("content\n\n", content)

    
        
    