import os
from dotenv import load_dotenv
load_dotenv()
import openai
from flask import Flask, request, render_template, session,Response
import uuid
from llmchain import llmchain
from gpt.bot import ask_corporation_bot, ask_engage_bot
from datetime import timedelta
from flask_session import Session
from flask_cors import CORS


# set the key
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__, instance_relative_config=True)
CORS(app)
app.secret_key = 'simple'
app.config['SESSION_TYPE'] = 'filesystem'
#app.permanent_session_lifetime = timedelta(minutes=5)
Session(app)

@app.route('/corporationbot', methods=['POST', 'GET'])
def corporationbot():
    query = request.form.get('query')
    user_id = request.remote_addr
    response = {}
    if query:
        response = ask_corporation_bot(query, user_id)
        
    return render_template('index.html', response=response.get('response'))


    

@app.route('/engagebot', methods=['POST', 'GET'])
def engagebot():
    query = request.json.get('query')
    session_id = request.json.get('session_id')
    if session_id:
        user_id = session_id
    elif 'session_id' in session:
        # Retrieve the user's data from the session
        user_id = session['session_id']
    else:
        # Generate a new session ID and store it in the session
        session['session_id'] = str(uuid.uuid4())
        user_id = session['session_id']
    
    if query:
        #response = llmchain.ask_corporation_bot(query)
        response = ask_engage_bot(query, user_id)
        response.update({'session_id' : user_id})
        return response

    else:
        message = {
            'message' : 'incorrect input',
            'session_id' : user_id
        }
        return Response(str(message), status=400,mimetype='application/json' )
        
    
    #response = llmchain.ask_corporation_bot(query)
    
# @app.route('/corporationbot', methods=['POST', 'GET'])
# def corporationbot():
#     return render_template('index.html')


if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug = True)