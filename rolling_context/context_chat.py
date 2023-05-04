
from typing import Any
from rolling_context.chat_store.sqlite import util as db_util
from rolling_context import gpt_util


WINDOW_SIZE = 6


def put_turn(user_id : Any, user_query : str, bot_response : str, delimiter : str = "###"):
    """
    Append the conversation turn into the allchat column of chatsummary table
    """
    turn = f"\nuser : {user_query} \n bot : {bot_response} \n{delimiter}\n"
    
    # print(dbUtil.get_allchat(0))
    db_util.append_to_all_chat_and_lastnturns(user_id, turn)

    last_n_turns = db_util.get_last_n_turns(user_id).strip()
    turns = last_n_turns.split(delimiter)
    turns = [t for t in turns if t != '']
    current_summary = db_util.get_summary(user_id)

    n = len(turns)

    if n == WINDOW_SIZE:
        ### TODOmove to fire thread
        summary = gpt_util.summarize_text(current_summary, last_n_turns)
        # flush the 60 % of turns from all_chat
        num_items = int(len(turns) * 0.4)
        recent_turns = turns[-num_items:]
        new_n_turns = delimiter.join(recent_turns)+ delimiter
        db_util.set_last_n_turns(user_id, new_n_turns)
        db_util.set_summary(user_id, summary)
        ###


def get_augmented_prompt(user_id : str, query : str):
    summary = db_util.get_summary(user_id)
    last_n_turns = db_util.get_last_n_turns(user_id)
    prompt_template = f"""
    summary of current user conversation is - '{summary}'
    
    recent conversation turns are - '{last_n_turns}'

    consider only system context, summary, recent conversation answer the below query else say I don't know

    query - '{query}'
    """

    return prompt_template






















