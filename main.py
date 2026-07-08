#########################
# MAIN Tkinter BRANCH   #
#########################

##### IMPORT STATEMENTS #####
import psycopg2
import ui
from tkinter import *

connection_string = "dbname=questlog user=postgres password=password host=localhost port=5432"
database_connection = None

try:
    # 1. Connect to the database
    print("Connecting to database...")
    database_connection = psycopg2.connect(connection_string)
    if database_connection:
        print("Successfully connected to database.")

    # 3. Draw UI
    root = Tk()
    root.title("Quest Log")
    root.geometry("650x800")
    program = ui.questlog_view(root, database_connection)

    #Start the main events loop
    print("DEBUG: Launching GUI...")
    program.build()
    print("DEBUG: Successfully launched GUI.")
    root.mainloop()

except Exception as e:
    print(f"Error: {e}")

finally:
    if database_connection and not database_connection.closed:
        database_connection.close()
        print("Database connection safely closed.")