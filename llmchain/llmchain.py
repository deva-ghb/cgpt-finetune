from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain import OpenAI
import sys
import os

# load OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = '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'


def construct_index(file_path, save_path):
  """
  file_path - path to document
  save_path - path to save the json including file name
  """
  # set maximum input size
  max_input_size = 4096
  # set number of output tokens
  num_outputs = 256
  # set maximum chunk overlap
  max_chunk_overlap = 20
  # set chunk size limit
  chunk_size_limit = 600

  prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

  # define LLM
  llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-ada-001", max_tokens=num_outputs))
  
  documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
  
  index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
  
  index.save_to_disk(save_path)
  
  return index


def ask_bot(input_index = 'index.json'):
  index = GPTSimpleVectorIndex.load_from_disk(input_index)
  query = input('What do you want to ask the bot?   \n')
   
  response = index.query(query, response_mode="compact")
  print("document chunks being used \n", response.source_nodes, "\n\n")
  print ("\nBot says: \n\n" + response.response + "\n\n\n")
 
    

if __name__ == "__main__":
  #construct_index("documents/mobile phone/Nokia 6310 User Guide only content.pdf", "built_indexes/index.json")
  ask_bot("built_indexes/index.json")


