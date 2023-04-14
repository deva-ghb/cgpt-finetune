from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.llms import OpenAI, OpenAIChat
from langchain.chat_models import ChatOpenAI
from langchain.indexes import VectorstoreIndexCreator

from gpt_index.langchain_helpers.text_splitter import TextSplitter
import os
from dotenv import load_dotenv
from typing import Any, Callable, Dict, List, Optional, Sequence, cast

load_dotenv("./.env")

# load OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = os.environ.get('OPENAI_API_KEY')

# Custom TextSplitter
class QATextSplitter(TextSplitter):
    """Implementation of splitting mulitple QA text."""

    def __init__(self, separator: str = "\n\n", **kwargs: Any):
        """Create a new TextSplitter."""
        super().__init__(**kwargs)
        self._separator = separator

    def split_text(self, text: str) -> List[str]:
        """Split incoming text and return chunks."""
        # First we naively split the large input into a bunch of smaller ones.
        if self._separator:
            splits = text.split(self._separator)
        else:
            splits = list(text)
        return self._merge_splits(splits, self._separator)

def construct_index(dir_path, save_path):
  """
  file_path - path to document
  save_path - path to save the json including file name
  """
  # set maximum input size
  max_input_size = 2000
  # set number of output tokens
  num_outputs = 256
  # set maximum chunk overlap
  max_chunk_overlap = 20
  # set chunk size limit
  chunk_size_limit = 600
  prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

  # define LLM
  llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=1000))
  
  documents = SimpleDirectoryReader(input_dir = dir_path).load_data()
  index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, 
                               prompt_helper=prompt_helper,
                               #text_splitter = QATextSplitter(separator="Q:")
                               )
  
  index.save_to_disk(save_path)
  return index


def ask_bot(input_index = 'index.json'):
  llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=1000))
  index = GPTSimpleVectorIndex.load_from_disk(input_index, llm_predictor = llm_predictor, similarity_top_k = 2)

  #data_dict = json.load(open("./built_indexes/Corporation_FAQ.json")).get('vector_store').get('simple_vector_store_data_dict')
  #resp = simple.SimpleVectorStore(data_dict).query([1 for _ in range(1536)], 1)
  #print(resp)
  # set the llm predictor
  # index.llm_predictor = LLMPredictor(llm=OpenAIChat(temperature=0, model_name="gpt-turbo-3.5", max_tokens=1000))
  print("model name", index.llm_predictor._llm.model_name)
  query = input('What do you want to ask the bot?   \n')
  #print("index struct", type(index.query))
  response = index.query(query, response_mode="compact")
  print("document chunks being used \n", response.source_nodes, "\n\n")
  print ("\nBot says: \n\n" + response.response + "\n\n\n")


def ask_engage_bot(query, input_index = 'index.json'):
  index = GPTSimpleVectorIndex.load_from_disk(input_index)
  response = index.query(query, response_mode="compact")
  return {
    'response' : response.response,
  }


def ask_and_carry_context_corportation_bot(query, user_id, input_index = "built_indexes/engage.json"):
   pass
   
   
   





def ask_corporation_bot(query ,input_index = 'built_indexes/Corporation_FAQ.json'):
  index = GPTSimpleVectorIndex.load_from_disk(input_index)
  #query = input('What do you want to ask the bot?   \n')
  response = index.query(query, response_mode="compact")
  # print('response', response.extra_info)
  # print("document chunks being used \n", response.source_nodes, "\n\n")
  # print ("\nBot says: \n\n" + response.response + "\n\n\n")

  return {
    'response' : response.response,
  }
    

if __name__ == "__main__":
  #construct_index("documents/Engage", "built_indexes/demo2.json")
  #ask_bot("built_indexes/Corporation_FAQ.json")
  ask_bot("built_indexes/demo.json")


