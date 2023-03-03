import sqlite3
from gpt import gptUtil

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
    select chatsummary from chatsummary where userid = {userid}
    """
    cursor = conn.execute(query)
    text = cursor.fetchone()
    conn.close()
    if text:
        return text[0]
    return ""

def get_allchat(userid):
    conn = create_connection(DB_PATH)
    query = f"""
    select allchat from chatsummary where userid = {userid}
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
        VALUES ({userid}, '{text}', '{text}')
        ON CONFLICT (userid) DO
        UPDATE 
        SET chatsummary = chatsummary || ' {text}',
        allchat = allchat || ' {text}'
        ;
    """
    conn = create_connection(DB_PATH)
    conn.execute(query)
    conn.commit()
    conn.close()


def update_summary(userid, new_summary):
    query = f"""
        UPDATE chatsummary 
        SET chatsummary = '{new_summary}'
        where userid = {userid}
        ;
    """
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
