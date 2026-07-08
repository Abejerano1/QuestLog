#########################
# MAIN Tkinter BRANCH   #
#########################

##### IMPORT STATEMENTS #####
import psycopg2
import ui
import user
from tkinter import *

connection_string = "dbname=questlog user=postgres password=password host=localhost port=5432"
database_connection = None

try:
    # 1. Connect to the database
    print("Connecting to database...")
    database_connection = psycopg2.connect(connection_string)

    if database_connection:
        print("Successfully connected to database!")

    # 2. Load current user info
    # DUMMY INFO:
    current_user = user.User(1,
                             "Merlin",
                             28,
                             9001,
                             "Mage",
                             "Technomancer",
                             database_connection=database_connection)

    # 3. Draw UI
    root = Tk()
    root.title("Quest Log")
    root.geometry("650x800")

    # Pass connection into UI view
    program = ui.questlog_view(root, database_connection)

    #Start the main events loop
    print("DEBUG: Launching GUI...")

    program.build(current_user)
    print("DEBUG: Successfully launched GUI.")
    root.mainloop()

except Exception as e:
    print(f"main.py: Error: {e}")

finally:
    if database_connection and not database_connection.closed:
        database_connection.close()
        print("Database connection safely closed.")