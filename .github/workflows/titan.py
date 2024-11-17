import psycopg2
from datetime import datetime
import schedule
import time

# Database connection parameters
DATABASE_URL = "postgres://u65r3b5s8m85kd:p5e46844d5c895f0e5394aa710fa143e1b3f0ebaca8b494b491a6322c8c7442de@c7t0sffab2p4bc.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d9h1hlaafrv484"

# Define the task to run at 1 AM
def daily_task():
    # Get the current date and convert to 'YY-MM-DD' format
    current_date = datetime.now().strftime("%Y-%m-%d")
    date_short = datetime.now().strftime("%y:%m:%d")
    
    # SQL queries
    check_query = f"SELECT * FROM dataturn WHERE Datet = '{date_short}'"
    
    delete_query = f"DELETE FROM dataturn WHERE Datet = '{date_short}'"

    try:
        


        
        # Connect to the database
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Check if data exists
        cur.execute(check_query)
        rows = cur.fetchall()
    
        cur.execute(delete_query)
        conn.commit()


        if rows:
            print(f"Data exists for date {date_short}. Running delete query...")
            cur.execute(delete_query)
            conn.commit()
            print(f"Data deleted for date {date_short}.")
        else:
            print(f"No data found for date {date_short}. No action taken.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")

daily_task()
