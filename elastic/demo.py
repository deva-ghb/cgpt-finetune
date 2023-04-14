# from elasticsearch import Elasticsearch

# es = Elasticsearch(hosts=["https://localhost:9200"],
#                   ca_certs='http_ca.crt',
#                   basic_auth=('elastic', 'rXxt3q+g+TLTej_XJ16f')
#                 )


# es.indices.create(index='first_index')

# # res = es.search(index="index", body={"query": {"match_all": {}}})
# # print(res)
# index_settings = {
#     "settings": {
#         "number_of_shards": 1,
#         "number_of_replicas": 0
#     },
#     "mappings": {
#         "properties": {
#             "title": {"type": "text"},
#             "content": {"type": "text"}
#         }
#     }
# }

# # create the index with the specified settings and mappings
# # es.indices.create(index="myindex"

# get the indices

# indices = es.indices.get_alias().keys()

# print("indices", indices)


# es.index(index="myindex", id=1, body={"title": "Hello", "content": "World"})

# # get a document by ID
# res = es.get(index="myindex", id=1)
# print("response", res)


from elasticsearch import Elasticsearch
import json

# Create an Elasticsearch client object
es = Elasticsearch(['http://localhost:9200'])

# indices = es.indices.get_alias().keys()

# print("indices ", indices

indices = es.indices.get_alias().keys()

# print the list of indexes
print(list(indices))

# res = es.search(index="5b97aaae244449dc898ee4f020ccda4f", body = {
# 'size' : 100,
# 'query': {
#     'match_all' : {}
# }
# })


# res_dict = dict(res)

# with open("my_dict.json", "w") as f:
#     json.dump(res_dict, f)


# Index a document
# doc = {'foo': 'bar'}
# res = es.index(index='my_index', body=doc)

# Search for documents

