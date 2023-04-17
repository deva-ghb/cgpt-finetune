# from context import context_chat
# context_chat.put_turn(0, user_query='what is ether?', bot_response='I dont know.')
from elastic.elastic_langchain import query_elastic_search_vector_index, load_index_to_elastic

# print(query_elastic_search_vector_index(index= '5b97aaae244449dc898ee4f020ccda4f',
#                                   query='best selling',
#                                   k = 1))

#load_index_to_elastic(dir_path='documents/Engage', index_name= 'good_index')
# load_index_to_elastic(dir_path='documents/FAQ', index_name='corporation_index', separator='Q:', drop_if_exist = True)
# load_index_to_elastic(dir_path='documents/Engage', index_name='engage_index', drop_if_exist = True)
print(query_elastic_search_vector_index(index = 'engage_index', query= 'how to add agent', k = 2))


# from gpt.corporation_bot import ask_corporation_bot
# from db.dbUtil import demo

# ask_corporation_bot('explain about registered agent', user_id='demo_3')

# # demo()