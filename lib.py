from tkinter import *
from tkinter import messagebox

import Objs
from Objs import *
import json


def add_quest(entry_field, quest_listbox, side_panel_contents, quest_history_listbox):
    # Stores selected quest
    quest = entry_field.get()

    if not quest:
        messagebox.showerror(title="Warning!", message="Please enter a quest.")
    else:
        name = quest
        # Creates new quest object
        new_quest = Quest(name, 10)
        # Inserts quest at the end of main listbox
        quest_listbox.insert(END, new_quest)
        # Clears entry field
        entry_field.delete(0, END)
        # Updates the stats panel
        update_side_panel(side_panel_contents, quest_listbox, quest_history_listbox)


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


def complete_quest(quest_listbox, side_panel_contents,
                   quest_history_listbox, entry_field):
    index = quest_listbox.curselection()
    if not index:
        messagebox.showwarning(title="Warning!", message="You must select a quest!")
    else:
        index = quest_listbox.curselection()
        # Gets the actual Quest object
        quest = quest_listbox.get(index)
        # Sends quest to history window
        add_quest_history(quest, quest_history_listbox)
        # Updates side panel
        #update_side_panel(side_panel_contents, quest_listbox, quest_history_listbox)
        # Removes quest from main window
        del_quest(quest_listbox, side_panel_contents, quest_history_listbox)
        entry_field.delete(0, END)

def update_user_header():
    username = get_attribute("username")

#Initializes the stats panel with default values
def initialize_side_panel(side_panel_contents):
    text1 = "INCOMPLETE QUESTS: 0"
    text2 = "COMPLETE QUESTS: 0"
    text3 = "TOTAL QUESTS: 0"
    side_panel_contents.insert(END, text1)
    side_panel_contents.insert(END, text2)
    side_panel_contents.insert(END, text3)


#Updates the data displayed on the stats panel (left)
def update_side_panel(side_panel_contents, quest_listbox, quest_history_listbox):
    complete = quest_history_listbox.size()
    incomplete = quest_listbox.size()
    total = complete + incomplete

    if quest_history_listbox.size() >= 0:
        # Update the side panel
        side_panel_contents.delete(0, END)

        line1 = f"INCOMPLETE QUESTS: {incomplete}"
        line2 = f"COMPLETE QUESTS: {complete}"
        line3 = f"TOTAL QUESTS: {total}"

        side_panel_contents.insert(END, line1)
        side_panel_contents.insert(END, line2)
        side_panel_contents.insert(END, line3)


#Adds a quest to the history panel (bottom of window)
def add_quest_history(quest, quest_history_listbox):
    quest_history_listbox.insert(END, quest)

#Loads a random profile (for testing purposes)
def load_random():
    pass

def get_attribute(attribute_name):
    profile_data = Objs.load_user_profile()

    if attribute_name in profile_data:
        return profile_data[attribute_name]
    else:
        return None