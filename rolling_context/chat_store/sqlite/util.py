
import sqlite3
DB_PATH = "rolling_context/chat_store/sqlite/chat.db"

from sqlalchemy import create_engine, text, select, Column, Integer, String, update
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Chat(Base):
    __tablename__ = 'chatsummary'
    user_id = Column(String, primary_key=True)
    all_chat = Column(String)
    last_n_turns = Column(String)
    summary = Column(String)
    

def get_summary(userid):
    engine = create_engine('sqlite:///{}'.format(DB_PATH))
    with Session(engine) as session:
        stmt = select(Chat.summary).where(Chat.user_id == userid)
        result = session.execute(stmt).fetchone()

    if result:
        return result[0]
    return ""



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

# def get_summary(userid):
#     conn = create_connection(DB_PATH)
#     query = f"""
#     select summary from ChatSummary where user_id = "{userid}";
#     """
#     cursor = conn.execute(query)
#     text = cursor.fetchone()
#     conn.close()
#     if text:
#         return text[0]
#     return ""

# def set_summary(user_id, summary):
#     conn = create_connection(DB_PATH)
#     conn.execute(f"""UPDATE ChatSummary SET summary="{summary}" WHERE user_id="{user_id}";""")
#     conn.commit()
#     conn.close()

def set_summary(user_id, summary):
    engine = create_engine('sqlite:///{}'.format(DB_PATH))
    with Session(engine) as session:
        session.query(Chat).filter(Chat.user_id == user_id).update({'summary': summary})
        session.commit()
    

def set_last_n_turns(user_id, last_n_turns):
    engine = create_engine('sqlite:///{}'.format(DB_PATH))
    with Session(engine) as session:
        session.query(Chat).filter(Chat.user_id == user_id).update({'last_n_turns': last_n_turns})
        session.commit()



def get_all_chat(userid):
    engine = create_engine('sqlite:///{}'.format(DB_PATH))
    with Session(engine) as session:
        stmt = select(Chat.all_chat).where(Chat.user_id == userid)
        result = session.execute(stmt).fetchone()

    if result:
        return result[0]
    return ""



# def clear_summary(userid):
#     conn = create_connection(DB_PATH)
#     query = f"""
#        UPDATE chatsummary 
#        SET chatsummary = '', allchat = ''
#        where userid = {userid}
#     """
#     cursor = conn.execute(query)
#     conn.commit()
#     conn.close()




# def append_to_summary(userid, text):
#     #currText = current_text(0)
#     query = f"""
#         INSERT INTO chatsummary (userid, chatsummary, allchat)
#         VALUES ({userid}, "{text}", "{text}")
#         ON CONFLICT (userid) DO
#         UPDATE 
#         SET chatsummary = chatsummary || " {text}",
#         allchat = allchat || " {text}"
#         ;
#     """
#     conn = create_connection(DB_PATH)
#     conn.execute(query)
#     conn.commit()
#     conn.close()

# def append_to_all_chat_and_lastnturns(user_id, text):
#     query = f"""
#         INSERT INTO chatsummary (user_id, last_n_turns, all_chat)
#         VALUES ("{user_id}", "{text}", "{text}")
#         ON CONFLICT (user_id) DO
#         UPDATE 
#         SET all_chat = all_chat || " {text}",
#         last_n_turns = last_n_turns || " {text}"
#         ;
#     """
#     conn = create_connection(DB_PATH)
#     conn.execute(query)
#     conn.commit()
#     conn.close()
def append_to_all_chat_and_lastnturns(user_id, text_value):
    engine = create_engine('sqlite:///{}'.format(DB_PATH))
    with Session(engine) as session:
        stmt = text("""
            INSERT INTO ChatSummary (user_id, last_n_turns, all_chat, timestamp)
            VALUES (:user_id, :text, :text, :timestamp)
            ON CONFLICT (user_id) DO
            UPDATE 
            SET all_chat = all_chat || ' ' || :text,
            last_n_turns = last_n_turns || ' ' || :text,
            timestamp = :timestamp
        """)
        session.execute(stmt, {"user_id": user_id, "text": text_value, "timestamp": datetime.now()})
        session.commit()

def get_last_n_turns(user_id):
    engine = create_engine('sqlite:///{}'.format(DB_PATH))
    with Session(engine) as session:
        stmt = select(Chat.last_n_turns).where(Chat.user_id == user_id)
        result = session.execute(stmt).fetchone()

    if result:
        return result[0]
    return ""





# def update_summary(userid, new_summary):
#     query = f"""
#         UPDATE chatsummary 
#         SET chatsummary = "{new_summary}"
#         where userid = {userid}
#         ;
#     """
#     conn = create_connection(DB_PATH)
#     conn.execute(query)
#     conn.commit()
#     conn.close()


def demo():
    query = f'''CREATE TABLE ChatSummary
             (user_id TEXT PRIMARY KEY,
             all_chat TEXT,
             last_n_turns TEXT,
             summary TEXT);'''
    q2 = "ALTER TABLE chatsummary ADD COLUMN timestamp DATETIME DEFAULT '1970-01-01 00:00:00'"
    conn = create_connection(DB_PATH)
    conn.execute(q2)
    conn.commit()
    conn.close()


# def summarize_current_chat(userid):
#     currText = get_summary(userid)
#     summary = gptUtil.summarize_as_two_parts(currText)
#     update_summary(userid, summary)


if __name__ == "__main__" :
    #clear_summary(0)
    #append_to_summary(1, "new text")
    #summarize_current_chat(0)

    print("hello world")
