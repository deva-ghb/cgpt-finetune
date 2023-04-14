##  capture the history
## 
from typing import Any
from db import dbUtil
from gpt import gptUtil


WINDOW_SIZE = 6


def put_turn(user_id : Any, user_query : str, bot_response : str, delimiter : str = "###"):
    """
    Append the conversation turn into the allchat column of chatsummary table
    """
    turn = f"\nuser : {user_query} \n bot : {bot_response} \n{delimiter}\n"
    
    # print(dbUtil.get_allchat(0))
    dbUtil.append_to_allchat_and_lastnturns(user_id, turn)

    last_n_turns = dbUtil.get_last_n_turns(user_id).strip()
    turns = last_n_turns.split(delimiter)
    turns = [t for t in turns if t != '']
    current_summary = dbUtil.get_summary(user_id)

    n = len(turns)

    if n == WINDOW_SIZE:
        ### move to fire and return thread
        summary = gptUtil.summarize_text(current_summary, last_n_turns)
        # flush the 60 % of turns from all_chat
        num_items = int(len(turns) * 0.4)
        recent_turns = turns[-num_items:]
        new_n_turns = delimiter.join(recent_turns)+ delimiter
        dbUtil.set_last_n_turns(user_id, new_n_turns)
        dbUtil.set_summary(user_id, summary)
        ###


def get_augmented_prompt(user_id : str, query : str):
    summary = dbUtil.get_summary(user_id)
    last_n_turns = dbUtil.get_last_n_turns(user_id)
    prompt_template = f"""
    summary of current user conversation is - {summary}
    
    recent conversation turns are - {last_n_turns}

    consider only system context, summary, recent conversation answer the below query else say I don't know

    query - {query}
    """

    return prompt_template



















