import psycopg2
from datetime import datetime
import time

# Database connection parameters

DATABASE_URL_TITAN = "postgres://u441pvtd8e6vts:p9915005381a379a3cf248f96097c48d4f64a005bb8e1cf01ac201eceb7a12967@c8lj070d5ubs83.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dekn82da4aom33"
DATABASE_URL_STARSTRIP = "postgres://u4okmvdq8me96b:p9a7af23f37abb06398c8f02b53f67d6f5efb57099b6459fe424ba65185b8f9ce@ce5cavigtak40n.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d4irea1nc6ba3h"
DATABASE_URL_CROWN = "postgres://udvr6gbrdfptkb:peb1123169c4deca93379cd55d913dbc347693820c19dd55f120185a6bcff6850@cd1jo1mf6mehgh.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d357hseirb9lm1"
DATABASE_URL_CLASSICNAIL = "postgres://ufhi4dfpt95dvn:p9aa11df4c8ab121a3d734e26d888961efecf2109bde5d978c9b54edee29fdead@c5flugvup2318r.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d3ev69nu274ni2"

# create list of database_url

#db_url = [DATABASE_URL_TITAN, DATABASE_URL_STARSTRIP, DATABASE_URL_CROWN, DATABASE_URL_CLASSICNAIL]

db_url = {
    "titan": DATABASE_URL_TITAN,
    "starstrip": DATABASE_URL_STARSTRIP,
    "crown":DATABASE_URL_CROWN,
    "classic":DATABASE_URL_CLASSICNAIL
}

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

def backup(alias, url):

    # SQL queries
    backup_query = """
        INSERT INTO backup (datet, vl)
        SELECT datet, vl FROM dataturn
        ON CONFLICT (datet) DO NOTHING;
    """


    try:
        # Connect to the database
        conn = psycopg2.connect(url)
        cur = conn.cursor()

        # Copy data from `backup` to `dataturn`
        cur.execute(backup_query)
        conn.commit()
        print(f"Data from dataturn was backup to backup table for {alias}")


        # Close the connection
        cur.close()
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")

for alias, url in db_url.items():
    backup(alias, url)

#daily_task()
