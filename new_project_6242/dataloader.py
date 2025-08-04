import pandas as pd
import sqlite3
import numpy as np
def load_user_listen_history():
    df = pd.read_csv("data/User_Listening_History.csv")
    df2 = df.groupby(['track_id','user_id'])['playcount'].sum().sort_values(ascending=False).reset_index()
    conn = sqlite3.connect('C:\\Users\\xxx\\xxx\\Desktop\\database\\6242')
    print(df2.head(10))
    try:
        conn.cursor().execute("DROP TABLE user_listen_history;")
        df2.to_sql('user_listen_history', conn, schema = "test", index=False, if_exists='append')
    except Exception as e:
        print(e)
    finally:
        conn.close()

def load_music_info():
    df = pd.read_csv("data/Music_Info.csv")
    conn = sqlite3.connect('C:\\Users\\xxx\\xxx\\Desktop\\database\\6242')
    try:
        conn.cursor().execute("DROP TABLE music_info;")
        df.to_sql('music_info', conn, schema = "test", index=False, if_exists='append')
    except Exception as e:
        print(e)
    finally:
        conn.close()




if __name__ == "__main__":
    load_music_info()