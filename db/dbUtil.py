import sqlite3
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
    conn = create_connection("./chatbot.db")
    query = f"""
    select chatsummary from chatsummary where userid = {userid}
    """
    cursor = conn.execute(query)
    text = cursor.fetchone()
    conn.close()
    if text:
        return text[0]
    return ""


def clear_summary(userid):
    conn = create_connection("./chatbot.db")
    query = f"""
       UPDATE chatsummary 
       SET chatsummary = ''
       where userid = {userid}
    """
    cursor = conn.execute(query)
    conn.commit()
    conn.close()




def append_to_summary(userid, text):
    #currText = current_text(0)
    query = f"""
        INSERT INTO chatsummary (userid, chatsummary)
        VALUES ({userid}, '{text}')
        ON CONFLICT (userid) DO
        UPDATE SET chatsummary= chatsummary || ' {text}';
    """
    conn = create_connection("./chatbot.db")
    conn.execute(query)
    conn.commit()
    conn.close()



if __name__ == "__main__":
    clear_summary(1)
