from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory

from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
import os
from dotenv import load_dotenv

load_dotenv("./.env")


# load OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = os.environ.get('OPENAI_API_KEY')


# human_message_prompt = HumanMessagePromptTemplate(
#         prompt=PromptTemplate(
#             template="What is a good name for a company that makes {product}?",
#             input_variables=["product"],
#         )
#     )
# chat_prompt_template = ChatPromptTemplate.from_messages([human_message_prompt])
# chat = ChatOpenAI(temperature=0.9)
# chain = LLMChain(llm=chat,
#                  prompt=chat_prompt_template)
# print(chain.run("pineapple peach"))

from langchain.llms import OpenAI
from langchain.chains import ConversationChain

memory = ConversationBufferWindowMemory(k=2)
memory.save_context({"input": "hi"}, {"ouput": "whats up"})
memory.save_context({"input": "not much you"}, {"ouput": "not much"})


conversation_with_summary = ConversationChain(
    llm=OpenAI(temperature=0, model_name='text-ada-001'), 
    # We set a low k=2, to only keep the last 2 interactions in memory
    memory=memory, 
    verbose=True
)
print(conversation_with_summary.predict(input="oh, why so?"))

print(conversation_with_summary.predict(input="thats fine!"))

print("buffer", ConversationBufferWindowMemory.buffer)