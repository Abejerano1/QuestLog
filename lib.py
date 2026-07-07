import json
from tkinter import *
from tkinter import messagebox

import psycopg2
from psycopg2 import Error

# Global parallel list to improve implementation
parallel_list = []


def complete_quest(quest_listbox, side_panel_contents, quest_history_listbox):
    # Selects quest in listbox
    index = quest_listbox.curselection()
    # Debug print statement
    print(f"complete_quest - index: {index}")

    if not index:
        messagebox.showwarning(title="Warning!", message="You must select a quest!")
    else:
        # Gets the actual Quest object
        quest = quest_listbox.get(index)
        print(f"complete_quest - quest: {quest}")
        # Sends quest to history window
        add_quest_history(quest, quest_history_listbox)
        # Removes quest from main window
        del_quest(quest_listbox, side_panel_contents, quest_history_listbox)


def del_quest(quest_listbox, side_panel_contents, quest_history_listbox):
    # Stores selected quest
    selected_targets = quest_listbox.curselection()
    if not selected_targets:
        messagebox.showwarning(title="Warning!", message="You must make choices!")
    else:
        for index in selected_targets:
            quest_listbox.delete(index)
        update_side_panel(side_panel_contents, quest_listbox, quest_history_listbox)


def del_all_tasks(quest_listbox, side_panel_text):
    for quest in quest_listbox:
        quest_listbox.delete(0, END, quest)


#Adds a quest to the history panel (bottom of window)
def add_quest_history(quest, quest_history_listbox):
    # quest_history_listbox.insert(END, quest)
    return None


def get_user_info():
    try:
        # 1. Connect to the database
        connection = psycopg2.connect(
            user="postgres",
            password="password",
            host="localhost",
            database="questlog",
            port="5432")

        # 2. Create a new cursor object
        cursor = connection.cursor()

        # 3. Execute simple single row query by ID
        query = f"""
                    SELECT user_name, user_level, user_exp, user_class, user_spec
                    FROM questlog.users
                    WHERE user_id = 1;
                """
        cursor.execute(query)
        user_info = cursor.fetchone()
        return user_info

    except Error as e:
        print("Error while connecting to PostgreSQL", e)
        return None

    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    # with open("user1.json", "r") as file:
    # data = json.load(file)
    # result = data["user_profile"][0][f"{attribute_name}"]
    # return result

def update_stats_in_json(file_path: str, stat_name: str, value: int) -> None:
    # Load
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Modify
    stats = data["user_stats"][0]
    stats[f"{stat_name}"] += value

    # Save (rewrite file)
    with open("user1.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


