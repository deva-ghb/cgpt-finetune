from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI



from dotenv import load_dotenv

load_dotenv("./.env")


# loader = TextLoader('documents/FAQ/Corporation FAQ.txt')
# documents = loader.load()
# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# docs = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings()


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



def query_elastic_search_vector_index(index : str, query : str, k : int) -> ElasticVectorSearch:
    db =  ElasticVectorSearch(elasticsearch_url="http://localhost:9200", index_name = index, embedding = embeddings)
    docs = db.similarity_search(query, k)
    relevant_page_content = ""
    for d in docs:
        relevant_page_content += d.page_content + "\n"
    return relevant_page_content









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



