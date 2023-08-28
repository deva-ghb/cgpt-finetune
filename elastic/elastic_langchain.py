from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch
from langchain.document_loaders import TextLoader, DirectoryLoader, PDFMinerLoader
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationChain, SimpleSequentialChain
import openai
from typing import Any, List
from langchain.schema import Document


from dotenv import load_dotenv


load_dotenv("./.env")

import os
def prepare_elastic_url(elastic_address):
     return f"http://{os.environ.get('ELASTIC_USER')}:{os.environ.get('ELASTIC_PASSWORD')}@{elastic_address}"
    

def log(content : str):
  """Appends the given context to the file `test_log.txt`.

  Args:
    context: The context to append to the file.

  """
  with open("test_log.txt", "a") as f:
    f.write(content)

# loader = TextLoader('documents/FAQ/Corporation FAQ.txt')
# documents = loader.load()
# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# docs = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings()

def _default_script_query(query_vector: List[float]):
    return {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                "params": {"query_vector": query_vector},
            
            },
        }
    }
    

def similarity_search_with_scores(
    self,query: str, k: int = 4, **kwargs: Any
) -> List[Document]:
    """Return docs most similar to query.

    Args:
        query: Text to look up documents similar to.
        k: Number of Documents to return. Defaults to 4.

    Returns:
        List of Documents most similar to the query.
    """
    
    embedding = self.embedding.embed_query(query)
    script_query = _default_script_query(embedding)
    response = self.client.search(index=self.index_name, query=script_query)
    hits = [hit["_source"] for hit in response["hits"]["hits"][:k]]
    similarities_scores = [hit["_score"] - 1 for hit in response["hits"]["hits"][:k]]
    print('hits', hits[0]['metadata'])
    print('scores', similarities_scores)
    documents = [
        Document(page_content=hit["text"], metadata=hit["metadata"]) for hit in hits
    ]
    return documents, similarities_scores


def load_index_to_elastic(dir_path : str, index_name : str, separator = '\n\n', drop_if_exist = True):
    """
    Args :
        dir_path - 
    """
    loader = DirectoryLoader(dir_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0, separator= separator)
    docs = text_splitter.split_documents(documents)
    db = ElasticVectorSearch.from_documents(docs,
                                        embeddings,
                                        elasticsearch_url="http://localhost:9200",
                                        index_name = index_name
                                        )

def load_pdf_index_to_elastic(doc_path : str, index_name : str, separator = '\n\n'):
    loader = PDFMinerLoader(doc_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=600, chunk_overlap=0, separator= separator)
    docs = text_splitter.split_documents(documents)
    ElasticVectorSearch.from_documents(docs,
                                        embeddings,
                                        elasticsearch_url="http://localhost:9200",
                                        index_name = index_name
                                        )

def query_elastic_search_vector_index(index : str, query : str, k : int, threshold = 0.8) -> ElasticVectorSearch:
    db =  ElasticVectorSearch(elasticsearch_url= prepare_elastic_url("44.193.55.184:9200"), index_name = index, embedding = embeddings)
    # db =  ElasticVectorSearch(elasticsearch_url="http://localhost:9200", index_name = index, embedding = embeddings)
    #docs, scores = similarity_search_with_scores(db, query, k)
    docs = db.similarity_search(query, k)
    # print('docs', docs)
    # print('scores', scores)
    relevant_page_content = ""
    for d in docs:
        relevant_page_content += d.page_content + "\n"
    return relevant_page_content


def query_gpt(query : str, index_name : str):
    log('\n#####\n')
    log(f'\nquery - {query}n')
    log(f'\nindex_name - {index_name}n')
    
    relevant_content = query_elastic_search_vector_index(index_name, query, k = 1)
    log(f'\nrelevant_page_content - {relevant_content}n')
    prompt = PromptTemplate(
    template="context : {relevant_content} \n use the above context to answer the following query  : {query}.",
    input_variables=["relevant_content", "query"],
    )
    template = prompt.format(relevant_content = relevant_content, query = query)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature = 0,
        messages=[
                #{"role": "system", "content": "we are talking about pineapple, particulary pineapple with blue dots.."},
                {"role": "user", "content": template}
            ]
    )

    response = completion["choices"][0]["message"]["content"]
    log(f'\nresponse - {response}n')
    return response
    







def converse_buffer(query : str, index_name : str, k : int):
    # create or retrive - ConversationBuffer
    # get the relevant content from conversation
    #
    db =  ElasticVectorSearch(elasticsearch_url="http://localhost:9200", index_name = index_name, embedding = embeddings)
    docs = db.similarity_search(query, k)
    relevant_page_content = ''
    for d in docs:
        relevant_page_content += d.page_content + "\n"
    # create llm
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    chain = load_qa_chain(llm, chain_type="stuff")

    # res = chain.run(input_documents=docs, question=query)
    prompt=PromptTemplate(
    template="Relevant document content : {relevant_content} to {output_language}.",
    input_variables=["relevant_content", "output_language"],
    )
    # Conversation buffer
    conversation_with_summary = ConversationChain(
    llm=llm,
    # We set a very low max_token_limit for the purposes of testing.
    memory=ConversationSummaryBufferMemory(llm=llm, max_token_limit=100,
    verbose=True
    )
    )
    conversation_with_summary
    # overall_chain = SimpleSequentialChain(chains=[chain, conversation_with_summary], verbose=True)

    # # conversation_with_summary.predict(input="Hi, what's up?")
    # overall_chain.run(input_documents=docs, question=query,  llm=llm,
    # # We set a very low max_token_limit for the purposes of testing.
    # memory=ConversationSummaryBufferMemory(llm=llm, max_token_limit=100),
    # verbose=True
    # )
    # ConversationBuffer.predict(augumted_prompt)













# print("embedig", embeddings.embed_query(text="hello"))
# db = ElasticVectorSearch.from_documents(docs,
#                                         embeddings,
#                                         elasticsearch_url="http://localhost:9200",
#                                         index_name = 'my_index'
#                                         )

# db = 



# query = "what is non-profit corporations?"

# db = ElasticVectorSearch(elasticsearch_url="http://localhost:9200", index_name = '5b97aaae244449dc898ee4f020ccda4f', embedding = embeddings)
# docs = db.similarity_search(query)  

# # print("docs", docs)


# chain = load_qa_chain(ChatOpenAI(temperature=0), chain_type="stuff")
# res = chain.run(input_documents=docs, question=query)

# print("res", res)



