import os
from dotenv import load_dotenv
load_dotenv()
import openai
from flask import Flask, request, render_template, url_for
from llmchain import llmchain
from gpt.bot import ask_corporation_bot, ask_engage_bot


# set the key
openai.api_key = os.environ.get("OPENAI_API_KEY")



app = Flask(__name__, instance_relative_config=True)

@app.route('/corporationbot', methods=['POST', 'GET'])
def corporationbot():
    query = request.form.get('query')
    user_id = request.remote_addr
    response = {}
    if query:
        #response = llmchain.ask_corporation_bot(query)
        response = ask_corporation_bot(query, user_id)
        
    
    #response = llmchain.ask_corporation_bot(query)
    return render_template('index.html', response=response.get('response'))

@app.route('/engagebot', methods=['POST', 'GET'])
def engagebot():
    query = request.form.get('query')
    user_id = request.remote_addr
    response = {}
    if query:
        #response = llmchain.ask_corporation_bot(query)
        response = ask_engage_bot(query, user_id)
        
    
    #response = llmchain.ask_corporation_bot(query)
    return render_template('engage.html', response=response.get('response'))

# @app.route('/corporationbot', methods=['POST', 'GET'])
# def corporationbot():
#     return render_template('index.html')


if __name__ == "__main__":
    app.run(debug= True)