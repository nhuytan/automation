import psycopg2
from datetime import datetime
import time

# Database connection parameters
#DATABASE_URL = "postgres://u65r3b5s8m85kd:p5e46844d5c895f0e5394aa710fa143e1b3f0ebaca8b494b491a6322c8c7442de@c7t0sffab2p4bc.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d9h1hlaafrv484"
DATABASE_URL = "postgres://u441pvtd8e6vts:p9915005381a379a3cf248f96097c48d4f64a005bb8e1cf01ac201eceb7a12967@c8lj070d5ubs83.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dekn82da4aom33"

# Define the task to run at 1 AM
def daily_task():
    # Get the current date and convert to 'YY-MM-DD' format
    current_date = datetime.now().strftime("%Y-%m-%d")
    date_short = datetime.now().strftime("%y:%m:%d")
    
    # SQL queries
    check_query = f"SELECT * FROM dataturn WHERE Datet = '{date_short}'"
    
    #delete_query = f"DELETE FROM dataturn WHERE Datet = '{date_short}'"
    delete_query = f"DELETE FROM dataturn'"

    try:
        # Connect to the database
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Check if data exists
        cur.execute(check_query)
        rows = cur.fetchall()
        
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

def backup():

    # SQL queries
    backup_query = """
        INSERT INTO backup (datet, vl)
        SELECT datet, vl FROM dataturn
        ON CONFLICT (datet) DO NOTHING;
    """


    try:
        # Connect to the database
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Copy data from `backup` to `dataturn`
        cur.execute(backup_query)
        conn.commit()
        print("Data from dataturn was backup to backup table.")


        # Close the connection
        cur.close()
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")

backup()
daily_task()
