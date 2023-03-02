import os
from dotenv import load_dotenv
load_dotenv()
import openai
from flask import Flask, request
from db import dbUtil 


# set the key
openai.api_key = os.environ.get("OPENAI_API_KEY")



def ask_davinci(prompt, userId):
    preppended_prompt = None
    if userId:
        accumulated_text = dbUtil.get_summary(userId)
        # add current prompt to the 
        dbUtil.append_to_summary(userId, prompt)
        preppended_prompt = accumulated_text + prompt
    else:
        preppended_prompt = prompt
    response = openai.Completion.create(
                #model= "ada:ft-:mental-health-model-2022-12-26-06-44-14",
                model= "davinci:ft-personal:mental-health-model-2023-02-28-08-28-05",
                prompt= preppended_prompt,
                temperature=0.7,
                max_tokens=250
      )
    choice_text = response['choices'][0]['text']
    if userId:
        dbUtil.append_to_summary(userId, choice_text)
    return choice_text

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/ask', methods=['POST', 'GET'])
    def ask():
        prompt = request.json.get("prompt")
        userId = request.json.get("userId")
        chatgpt_response = ask_davinci(prompt, userId)
        response = {
            'completion' : chatgpt_response
        }
        return response

    return app


if __name__ == "__main__":
    create_app().run(port=5005, debug= True)

