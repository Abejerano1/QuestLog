from tkinter import *
from tkinter import messagebox
from Objs import *
from typing import Union
import json

# Global parallel list to improve implementation
parallel_list = []

"""
===================================================================================
STUBS:
===================================================================================
"""

# def initialize_profile(file_path, icon_path, user_header) -> None:

# def initialize_main_panel(file_path) -> None:

# def update_user_header(file_path) -> None:



"""
===================================================================================
IMPLEMENTATION:
===================================================================================
"""

def initialize_side_panel(file_path, side_panel_contents) -> None:
    """
    Initializes the side panel.

    :param file_path: The path to the target user file.
    :param side_panel_contents: The contents of the side panel.
    :return: None
    """

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Safely get the first stats object
    stats = data.get("user_stats", [{}])[0]
    # 1. Uses .get() on a dictionary (data)
    # 2. Provides a default value if the key isn't found "({})"
    # 3. Immediately accesses the first item "[0]" of the resulting list

    # Extract numeric values (will raise if missing or wrong type
    total = stats["total_quests"]
    active = stats["active"]
    completed = stats["completed"]
    incomplete = stats["incomplete"]
    failed = stats["failed"]

    side_panel_contents.insert(END, f"ACTIVE QUESTS: {active}")
    side_panel_contents.insert(END, f"COMPLETED QUESTS: {completed}")
    side_panel_contents.insert(END, f"INCOMPLETE QUESTS: {incomplete}")
    side_panel_contents.insert(END, f"FAILED QUESTS: {failed}")
    side_panel_contents.insert(END, f"TOTAL QUESTS: {total}")


def add_quest(file_path, entry_field, quest_listbox, side_panel_contents, quest_history_listbox) -> None:
    """
    Adds a quest to the main list.

    Args:
        :param entry_field: The entry widget where the quest name is entered.
        :param quest_listbox: The listbox widget displaying the list of quests.
        :param side_panel_contents: The side panel widget displaying the quest state.
        :param quest_history_listbox: The listbox widget displaying quest history.
        :param file_path: The file path where the quest state is stored.
        :return: None
    """

    # Stores selected quest
    quest_name = entry_field.get()
    if not quest_name:
        messagebox.showerror(title="Warning!", message="Please enter a quest.")
        return

    # Creates new quest object
    new_quest = Quest(quest_name, exp=10)
    parallel_list.append(new_quest) # keep the real object

    # Inserts quest at the end of main listbox
    quest_listbox.insert(END, new_quest) # store only the display string

    # Updates quest count in user JSON
    add_quest_to_json(file_path, new_quest)

    # Clears entry field
    entry_field.delete(0, END)

    # Updates the stats panel
    update_side_panel("user1.json", side_panel_contents, quest_listbox, quest_history_listbox)


def add_quest_to_json(file_path, quest) -> None:
    """
    Updates the JSON file with the new quest.

    Args:
        :param file_path: The path to the JSON file.
        :param quest: The quest object to be added.
        :return: None
    """

    try:
        # Load existing data from JSON file
        with open(file_path, "r+", encoding="utf-8") as file:
            data = json.load(file)

            # Ensure 'quests' is a list
            if "quests" not in data:
                data["quests"] = []

            # Append the new quest to the 'quests' list
            data["quests"].append(quest.to_dict())
            parallel_list.append(quest)

            for line in data.get("user_stats", []):
                line["active"] += 1
                line["total_quests"] += 1
                break

            # Moves file pointer back to the beginning of the file
            file.seek(0)
            # Writes "data" dictionary to the file in JSON format
            json.dump(data, file, indent=4)
            # Cuts off any content remaining in the file after the current
            # file pointer position.
            file.truncate()


    except FileNotFoundError:
        messagebox.showerror(title="Error", message="The specified file was not found.")
    except json.JSONDecodeError:
        messagebox.showerror(title="Error", message="Failed to decode JSON. The file may be corrupted.")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"An unexpected error occurred: {e}")


def complete_quest(quest_listbox, side_panel_contents, quest_history_listbox) -> None:
    """
    Removes the quest from the main panel and sends it to the quest history panel.

    :param quest_listbox: The main listbox containing active quests
    :param side_panel_contents: The statistics in the side panel listbox
    :param quest_history_listbox: The bottom listbox that contains completed quests.
    :return: None
    """

    # Selects quest in listbox
    selection = quest_listbox.curselection()
    # Debug print statement
    print(f"complete_quest - selection: {selection}")

    index: int = selection[0]
    print(f"complete_quest - selection index: {index}\n")

    if index < 0:
        messagebox.showwarning(title="Warning!", message="You must select a quest!")
    else:
        # Gets the actual Quest object
        quest = quest_listbox.get(index)
        print(f"complete_quest - quest: {quest}")
        # Sends quest to history window
        add_quest_history(quest, quest_history_listbox)
        # Updates quest in user JSON
        complete_quest_in_json("user1.json", index, selection)
        # Removes quest from main window
        # ALSO DECREMENTS QUEST ITEMS IN LIST
        del_quest(quest_listbox, side_panel_contents, quest_history_listbox)


def complete_quest_in_json(file_path, index: int, selection) -> None:
    """
    Marks quest as complete in user JSON file.

    :param file_path:
    :param index:
    :param selection:
    :return:
    """
    print(f"complete_quest_in_json - index: {index}")

    # Retrieve the actual Quest object from the parallel list
    quest_id = selection.get_quest_attribute("id_num")
    print(f"complete_quest_in_json - quest_id before: {quest_id}")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            # Debug print
            print(f"complete_quest_in_json - data:")
            for line in data["quests"]:
                print(line)

        for q in data.get("quests", []):
            if q.get("id_num") == quest_id:
                #Debug print
                print(f"JSON quest name: {q.get("name")}")
                # Updates the quest's completion status
                q["complete"] = True
                break
            else:
                messagebox.showwarning(title="Warning!", message="The quest ID number is invalid.")
                return

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    except FileNotFoundError:
        messagebox.showerror(title="Error", message="The specified file was not found.")
    except json.JSONDecodeError:
        messagebox.showerror(title="Error", message="Failed to decode JSON. The file may be corrupted.")
    except TypeError as e:
        messagebox.showerror(title="Error", message=f"TypeError: {e}")

    print(f"complete_quest_in_json - quest_id after: {quest_id}")


def del_quest(quest_listbox, side_panel_contents, quest_history_listbox) -> None:
    """
    Deletes a quest from the main panel.

    :param quest_listbox: The main listbox containing active quests.
    :param side_panel_contents: The statistics in the side panel listbox.
    :param quest_history_listbox: The bottom listbox that contains completed quests.
    :return: None
    """
    selected_targets = quest_listbox.curselection()
    if not selected_targets:
        messagebox.showwarning(title="Warning!", message="You must make choices!")
    else:
        for index in selected_targets:
            quest_listbox.delete(index)
        del_quest_in_json("user1.json", selected_targets)

        update_side_panel("user1.json", side_panel_contents, quest_listbox, quest_history_listbox)

def del_quest_in_json(file_path, selected_targets) -> None:
    """
    Deletes a quest from the JSON file.

    :param file_path: The path to the JSON file.
    :param selected_targets: The quest targeted for deletion.
    :return: None
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        for line in data.get("user_stats", []):
            line["total_quests"] -= 1
            line["active"] -= 1
            break

    except Exception as e:
        messagebox.showerror(title="Warning!", message=f"Failure in del_quest_in_json. {e}")

def del_all_tasks(quest_listbox) -> None:
    """
    Deletes all active quests.

    :param quest_listbox: The listbox containing active quests,
    :return: None
    """

    for quest in quest_listbox:
        quest_listbox.delete(0, END, quest)


#Updates the data displayed on the stats panel (left)
def update_side_panel(file_path, side_panel_contents, quest_listbox, quest_history_listbox) -> None:
    """
    Updates the side panel contents.

    :param file_path: The target user JSON file.
    :param side_panel_contents: The side panel contents.
    :param quest_listbox: The main listbox containing active quests.
    :param quest_history_listbox: The bottom listbox that contains completed quests.
    :return: None
    """

    complete = quest_history_listbox.size()
    incomplete = quest_listbox.size()


    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Safely get the first stats object
    stats = data.get("user_stats", [{}])[0]
    # 1. Uses .get() on a dictionary (data)
    # 2. Provides a default value if the key isn't found "({})"
    # 3. Immediately accesses the first item "[0]" of the resulting list

    if quest_history_listbox.size() >= 0:
        # Update the side panel
        side_panel_contents.delete(0, END)

        active = stats["active"]
        completed = stats["completed"]
        incomplete = stats["incomplete"]
        failed = stats["failed"]
        total = stats["total_quests"]

        side_panel_contents.insert(END, f"ACTIVE QUESTS: {active}")
        side_panel_contents.insert(END, f"COMPLETED QUESTS: {completed}")
        side_panel_contents.insert(END, f"INCOMPLETE QUESTS: {incomplete}")
        side_panel_contents.insert(END, f"FAILED QUESTS: {failed}")
        side_panel_contents.insert(END, f"TOTAL QUESTS: {total}")


#Adds a quest to the history panel (bottom of window)
def add_quest_history(quest: object, quest_history_listbox) -> None:
    quest_history_listbox.insert(END, quest)


#Loads a random profile (for testing purposes)
def load_random():
    pass


"""
####################################
            GETTERS
####################################
"""

def get_user_attribute(attribute_name: str) -> Union[str, int]:
    """
    Accesses a desired user attribute.

    :param attribute_name: The name of the desired attribute.
    :return: String or integer representing the desired attribute.
    """

    with open("user1.json", "r") as file:
        data = json.load(file)
    result = data["user_profile"][0][f"{attribute_name}"]
    return result

def get_user_stat(stat_name: str) -> Union[str, int]:
    """
    Accesses a desired user stat.

    :param stat_name: The name of the desired stat.
    :return: String or integer representation of stat.
    """

    with open("user1.json", "r") as file:
        data = json.load(file)
    result = data["user_stats"][0][f"{stat_name}"]
    return result

def qet_quest_attribute(attribute_name: str) -> int:
    """
    Accesses a desired quest attribute.

    :param attribute_name: The name of the quest attribute.
    :return: Integer representation of quest attribute.
    """

    with open("user1.json", "r") as file:
        data = json.load(file)
    result = data["quests"][0][f"{attribute_name}"]
    return result

def update_stats_in_json(file_path: str, stat_name: str, value: int) -> None:
    """
    Updates the stats in json file.

    :param file_path: The path to the json file.
    :param stat_name: The name of the stat to update.
    :param value: The value with which we are updating the stat
    :return: None
    """
    # Load
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Modify
    stats = data["user_stats"][0]
    stats[f"{stat_name}"] += value

    # Save (rewrite file)
    with open("user1.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)