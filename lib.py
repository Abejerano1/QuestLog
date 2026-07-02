import json
from tkinter import *
from tkinter import messagebox

import psycopg2
from psycopg2 import Error

# Global parallel list to improve implementation
parallel_list = []

def add_quest(user_id, entry_field, quest_listbox, side_panel_contents, quest_history_listbox, file_path) -> None:
    """
    Adds a quest to the main list.

    Args:
        :param entry_field:
        :param quest_listbox:
        :param side_panel_contents:
        :param quest_history_listbox:
        :param file_path:
        :return: None
    """

    # Stores selected quest
    quest_name = entry_field.get()
    quest_description = entry_field.get()
    quest_exp = entry_field.get()
    if not (quest_name, quest_description, quest_exp):
        messagebox.showerror(title="Warning!", message="Please enter a value.")
        return

    # # Creates new quest object
    # new_quest = Quest(quest_name, exp=10)
    # parallel_list.append(new_quest) # keep the real object
    #
    # # Inserts quest at the end of main listbox
    # quest_listbox.insert(END, str(new_quest)) # store only the display string
    #
    # # Clears entry field
    # entry_field.delete(0, END)
    #
    # # Updates the stats panel
    # # update_side_panel(side_panel_contents, quest_listbox, quest_history_listbox)


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
        # Updates quest in user JSON
        complete_quest_in_json("user1.json", index)
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


# def update_user_header():
    # username = get_user_info()
    # return username


#Initializes the stats panel with default values
def initialize_side_panel(user_id, side_panel_contents):
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
                    SELECT complete_quests, incomplete_quests, total_quests
                    FROM questlog.users
                    WHERE user_id = {user_id};
                """
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            complete_quests, incomplete_quests, total_quests = result
            side_panel_contents.insert(END, f"INCOMPLETE QUESTS: {incomplete_quests}")
            side_panel_contents.insert(END, f"COMPLETE QUESTS: {complete_quests}")
            side_panel_contents.insert(END, f"TOTAL QUESTS: {total_quests}")

    except Error as e:
        print("Error while connecting to PostgreSQL", e)
        return None

    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


# Updates the data displayed on the stats panel (left)
def update_side_panel(side_panel_contents, quest_listbox, quest_history_listbox):
    return None


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


