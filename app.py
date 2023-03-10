import os
from dotenv import load_dotenv
load_dotenv()
import openai
from flask import Flask, request
from db import dbUtil
from threading import Timer


# set the key
openai.api_key = os.environ.get("OPENAI_API_KEY")

SUMMARY_THRESHOLD = 600 #words
CONVERSATION_DELIMTTER = "$$$"


def ask_davinci(prompt, userId):
    preppended_prompt = None
    if userId is not None:
        accumulated_text = dbUtil.get_summary(userId)
        # add current prompt to the summary
        dbUtil.append_to_summary(userId, f"\nquestion : {prompt}\n")
        preppended_prompt = accumulated_text + prompt
    else:
        preppended_prompt = prompt
    

    response = openai.Completion.create(
                #model= "ada:ft-:mental-health-model-2022-12-26-06-44-14",
                model= "davinci:ft-personal:mental-health-model-2023-02-28-08-28-05",
                prompt= preppended_prompt,
                temperature=0.7,
                max_tokens=250,
                stop = ['.']
    )

    # check if threshold is reached and trigger the process to start 
    if userId is not None and len(preppended_prompt.split(" ")) >= SUMMARY_THRESHOLD:
        print("Threshold reached...")
        ## summarize..
        # retVal = Timer(
        #     3,
        #     dbUtil.summarize_current_chat,
        #     args=(userId,)).start()
    choice_text = response['choices'][0]['text']
    print("response..", choice_text)
    choice_text = choice_text.replace('"', "'")
    if userId is not None:
        dbUtil.append_to_summary(userId, f"response : {choice_text}\n{CONVERSATION_DELIMTTER}")
    return choice_text

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/ask', methods=['POST', 'GET'])
    def ask():
        prompt = request.json.get("prompt")
        userId = request.json.get("userId")
        print("got user id", userId)
        chatgpt_response = ask_davinci(prompt, userId)
        response = {
            'completion' : chatgpt_response
        }
        return response

    return app


if __name__ == "__main__":
    create_app().run(port=5005, debug= True)

