import pandas as pd
import psycopg2


def connect():
    print("Connecting to DB...")
    conn = psycopg2.connect(
        dbname="db_access_inventory",
        user="user",
        password="VerySecureYesYes123",
        host="localhost",
        port=5432
    )
    return conn

def is_table_empty(cursor):
    cursor.execute("SELECT COUNT(*) FROM activity;")
    result = cursor.fetchone()
    return result[0] == 0

df = pd.read_csv('dataset/inventary_csv.csv', delimiter='.')

conn = None
try:
    conn = connect()
    cursor = conn.cursor()
    
    if is_table_empty(cursor):
        print("Populating the Database")
        data = [tuple(row) for _, row in df.iterrows()]
        
        sql_insert_query = """INSERT INTO inventary
            (alchoolContent, availableVolume, batchID, beerStyle, brewDate, brewLocation, cost, expertScore, phLevel, userScore) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        cursor.executemany(sql_insert_query, data)
        conn.commit()
    else:
        print("Activity table is not empty. Skipping data insertion.")
except psycopg2.Error as error:
    print(error)
    conn.rollback()
finally:
    if conn is not None:
        conn.close()