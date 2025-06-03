from tkinter import *
from tkinter import messagebox
from Objs import Quest


def update_listbox(quest_listbox, quest_counter_label):
    pass

def add_task(quest_listbox, side_panel_text, quest):
    if quest:
        quest = Quest(quest, 10)
        quest_listbox.insert(END, quest)
    else:
        messagebox.showwarning(title="Warning!", message="You must enter a quest!")

    update_listbox(quest_listbox, side_panel_text)
    update_quest_count(quest_listbox, side_panel_text)

def del_task(quest_listbox, quest_counter_label):
    selected_targets = quest_listbox.curselection()
    if not selected_targets:
        messagebox.showwarning(title="Warning!", message="You must make choices!")
    else:
        for index in selected_targets:
            quest_listbox.delete(index)

    update_listbox(quest_listbox, quest_counter_label)
    update_quest_count(quest_listbox, quest_counter_label)

def del_all_tasks(quest_window):
    #iterate through listbox items
    #delete while iterating
    pass

def choose_random():
    pass

def update_quest_count(quest_listbox=None, side_panel_text=None):
    if quest_listbox is not None:
        count = quest_listbox.size()
        # Update the side panel
        side_panel_text.delete("1.0", END)
        updated_info = (f"TOTAL QUESTS: {count}"
                        f"\nINCOMPLETE QUESTS: {count}"
                        f"\nCOMPLETE QUESTS: 0")
        side_panel_text.insert(END, updated_info)
    else:
        side_panel_text.delete("1.0", END)
        updated_info = (f"TOTAL QUESTS: 0"
                        f"\nINCOMPLETE QUESTS: 0"
                        f"\nCOMPLETE QUESTS: 0")
        side_panel_text.insert(END, updated_info)