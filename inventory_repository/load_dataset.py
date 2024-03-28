import psycopg2
import os
import csv
import random

def __connect():
    print("Connecting to DB...")
    conn = psycopg2.connect(
        dbname=os.getenv('INVENTORY_DB_NAME'),
        user=os.getenv('INVENTORY_DB_USER'),
        password=os.getenv('INVENTORY_DB_PASSWORD'),
        host=os.getenv('INVENTORY_DB_HOST'),
        port=os.getenv('INVENTORY_DB_PORT')
    )
    return conn

def __is_table_empty(cursor):
    cursor.execute("SELECT COUNT(*) FROM inventory;")
    result = cursor.fetchone()
    return result[0] == 0

def __getCost():
    return round(random.uniform(5,30), 3)



def load():
    csvPath = os.getenv('DATASET_URL','./dataset/dataset.csv')

    conn = None
    try:
        conn = __connect()
        cursor = conn.cursor()

        print('Initiating DB...')

        cursor.execute("""CREATE TABLE IF NOT EXISTS inventory(
                       batch_id INTEGER,
                       brew_date DATE NOT NULL,
                       beer_style VARCHAR NOT NULL,
                       location VARCHAR NOT NULL,
                       ph_level NUMERIC(3,1) NOT NULL,
                       alcohol_content NUMERIC(3,1) NOT NULL,
                       volume_produced NUMERIC(6,1) NOT NULL,
                       quality_score NUMERIC(3,1) NOT NULL,
                       cost NUMERIC(3,1) NOT NULL,
                       user_score NUMERIC(3,1) NOT NULL,
                       n_users_review NUMERIC(3,1) NOT NULL,
                       PRIMARY KEY (batch_id)
        )""")

        conn.commit()
        
        if __is_table_empty(cursor):
            print("Populating the Database...")
            
            with open(csvPath, 'r') as f:
                
                n_rows = 0
                reader = csv.reader(f)
                next(reader) #Skip headers

                for row in reader:
                    
                    # Number of rows to be loaded
                    if(n_rows == 50):
                        break

                    clean_row = (int(row[0]), 
                                 str(row[1]), 
                                 str(row[2]), 
                                 str(row[4]), 
                                 float(row[7]), 
                                 float(row[9]), 
                                 float(row[13]), 
                                 float(row[15]), 
                                 float(__getCost()), 
                                 float(0),
                                 float(1))

                    print(n_rows, clean_row)
                    n_rows += 1

                    query = """INSERT INTO inventory VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

                    cursor.execute(query, clean_row)
                    conn.commit()
                
        else:
            print("Inventory table is not empty. Skipping data insertion.")
    except psycopg2.Error as error:
        print(error)
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()