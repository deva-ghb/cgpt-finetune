import sqlite3
from gpt import gptUtil
"""

create - uml diagram for maintaining chat context

chats table schema(userid, allChat, lastNTurns, summary)

put every turn in to allchat column
maintain the last N conversation turn in the lastNTurns column
once N turns reached summarize the turns and store summary in the summary column and flush the 60 % of conversation turns starting from oldest
this way last 40 % N conversation turns will always be maintained in its original form

context = {
current summary of the conversation  : <summary>
recent conversation turns : <last>
}


"""

DB_PATH = "./db/chatbot.db"
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return conn

def get_summary(userid):
    conn = create_connection(DB_PATH)
    query = f"""
    select summary from ChatSummary where user_id = "{userid}";
    """
    cursor = conn.execute(query)
    text = cursor.fetchone()
    conn.close()
    if text:
        return text[0]
    return ""

def set_summary(user_id, summary):
    conn = create_connection(DB_PATH)
    conn.execute(f"""UPDATE ChatSummary SET summary="{summary}" WHERE user_id="{user_id}";""")
    conn.commit()
    conn.close()


def set_last_n_turns(user_id, last_n_turns):
    conn = create_connection(DB_PATH)
    conn.execute(f"""UPDATE ChatSummary SET last_n_turns="{last_n_turns}" WHERE user_id="{user_id}";""")
    conn.commit()
    conn.close()


def get_allchat(userid):
    conn = create_connection(DB_PATH)
    query = f"""
    select all_chat from chatsummary where userid = "{userid}";
    """
    cursor = conn.execute(query)
    text = cursor.fetchone()
    conn.close()
    if text:
        return text[0]
    return ""



def clear_summary(userid):
    conn = create_connection(DB_PATH)
    query = f"""
       UPDATE chatsummary 
       SET chatsummary = '', allchat = ''
       where userid = {userid}
    """
    cursor = conn.execute(query)
    conn.commit()
    conn.close()




def append_to_summary(userid, text):
    #currText = current_text(0)
    query = f"""
        INSERT INTO chatsummary (userid, chatsummary, allchat)
        VALUES ({userid}, "{text}", "{text}")
        ON CONFLICT (userid) DO
        UPDATE 
        SET chatsummary = chatsummary || " {text}",
        allchat = allchat || " {text}"
        ;
    """
    conn = create_connection(DB_PATH)
    conn.execute(query)
    conn.commit()
    conn.close()

def append_to_allchat_and_lastnturns(user_id, text):
    query = f"""
        INSERT INTO chatsummary (user_id, last_n_turns, all_chat)
        VALUES ("{user_id}", "{text}", "{text}")
        ON CONFLICT (user_id) DO
        UPDATE 
        SET all_chat = all_chat || " {text}",
        last_n_turns = last_n_turns || " {text}"
        ;
    """
    conn = create_connection(DB_PATH)
    conn.execute(query)
    conn.commit()
    conn.close()

def get_last_n_turns(user_id):
    query = f"""SELECT last_n_turns FROM ChatSummary WHERE user_id="{user_id}";"""
    conn = create_connection(DB_PATH)
    conn.execute(query)
    result = conn.execute(query).fetchone()
    if result is not None:
        # Extract the last_n_turns value from the query result
        last_n_turns = result[0]
        return last_n_turns
    return ""





def update_summary(userid, new_summary):
    query = f"""
        UPDATE chatsummary 
        SET chatsummary = "{new_summary}"
        where userid = {userid}
        ;
    """
    conn = create_connection(DB_PATH)
    conn.execute(query)
    conn.commit()
    conn.close()


def demo():
    query = f'''CREATE TABLE ChatSummary
             (user_id TEXT PRIMARY KEY,
             all_chat TEXT,
             last_n_turns TEXT,
             summary TEXT);'''
    q2 = 'drop table ChatSummary'
    conn = create_connection(DB_PATH)
    conn.execute(query)
    conn.commit()
    conn.close()


def summarize_current_chat(userid):
    currText = get_summary(userid)
    summary = gptUtil.summarize_as_two_parts(currText)
    update_summary(userid, summary)


if __name__ == "__main__" :
    #clear_summary(0)
    #append_to_summary(1, "new text")
    #summarize_current_chat(0)

    print("hello world")
