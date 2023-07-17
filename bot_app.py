import os, json
from dotenv import load_dotenv
load_dotenv()
import openai
from flask import Flask, request, render_template, session,Response
import uuid
from llmchain import llmchain
from gpt.bot import ask_corporation_bot, ask_engage_bot
from formbuild_gpthelper.gpt.gptUtil import formSpecificationToJson
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
    

@app.route('/usecase-to-form', methods=['POST', 'GET'])
def form_builder():
    usecase = request.json.get('usecase')

    try:    
        if usecase:
            #response = llmchain.ask_corporation_bot(query)
            data = formSpecificationToJson(usecase)
            response = {
                "data" : data,
                "status" : "SUCCESS",
                "display_message" : "Response created.",
                "code" : 200
            }
            return Response(json.dumps(response), status=200, mimetype='application/json' )

        else:
            response = {
                "data" : None,
                "status" : "INCORRECT INPUT",
                "display_message" : "Supply the usecase.",
                "code" : 403,
            }
            return Response(json.dumps(response), status=403, mimetype='application/json' )
    
    except openai.error.Timeout as e:
        #Handle timeout error, e.g. retry or log
        print(f"OpenAI API request timed out: {e}")
        response = {
                "data" : None,
                "status" : "FAILED",
                "display_message" : "Timeout",
                "code" : 500,
            }
        pass
    except openai.error.APIError as e:
        #Handle API error, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        response = {
                "data" : None,
                "status" : "FAILED",
                "display_message" : "APIError",
                "code" : 500,
            }
        pass
    except openai.error.APIConnectionError as e:
        #Handle connection error, e.g. check network or log
        print(f"OpenAI API request failed to connect: {e}")
        response = {
                "data" : None,
                "status" : "FAILED",
                "display_message" : "APIConnectionError",
                "code" : 500,
            }
        pass
    except Exception as e:
        response = {
                "data" : {'fields' : []},
                "status" : "FAILED",
                "display_message" : f"Could not generate form.",
                "code" : 500,
        }

        return Response(json.dumps(response), status=500, mimetype='application/json' )


        
    
    #response = llmchain.ask_corporation_bot(query)
    
# @app.route('/corporationbot', methods=['POST', 'GET'])
# def corporationbot():
#     return render_template('index.html')


if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug = True, port = 5001)