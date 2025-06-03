from tkinter import *
from tkinter import messagebox
from Objs import Quest


def add_quest(quest, quest_listbox, side_panel_text, quest_list):
    if quest:
        name = quest
        # Creates new quest object
        new_quest = Quest(name, 10)
        quest_list.append(new_quest)
        # Inserts quest at the end of main listbox
        quest_listbox.insert(END, new_quest)

        update_side_panel(side_panel_text, quest_list)
    else:
        messagebox.showerror(title="Warning!", message="Please enter a quest.")

def del_quest(quest_listbox, quest_counter_label, quest_list):
    # Stores selected quest
    selected_targets = quest_listbox.curselection()
    if not selected_targets:
        messagebox.showwarning(title="Warning!", message="You must make choices!")
    else:
        for index in selected_targets:
            quest_listbox.delete(index)
            quest_list.delete(index)

    update_side_panel(quest_list, quest_listbox, quest_counter_label)

def del_all_tasks(quest_listbox, side_panel_text):
    for quest in quest_listbox:
        quest_listbox.delete(0, END, quest)


def complete_quest(quest_listbox, side_panel_text,
                   quest_history_listbox, quest_list, completed_list):
    quest_indices = quest_listbox.curselection()
    try:
        index = quest_indices[0]
        # Gets the actual Quest object
        quest = quest_list[index]

        # Marks quest as complete
        quest.complete = True
        completed_list.append(quest)
        # Sends quest to history window
        update_quest_history(quest, quest_history_listbox)
        # Updates side panel
        update_side_panel(quest_list, quest_listbox, side_panel_text)
        # Removes quest from main window
        del quest_list[index]
        quest_listbox.delete(index)
    except IndexError:
        messagebox.showwarning(title="Warning!", message="You must select a quest!")


def choose_random():
    pass

def update_side_panel(side_panel_text, quest_history_listbox, quest_listbox=None):
    if quest_listbox is not None:
        # Variable for quest count
        quest_count = quest_listbox.size()
        # variable for list
        completed_count = quest_history_listbox.size()

        # Update the side panel
        side_panel_text.delete("1.0", END)
        updated_info = (f"TOTAL QUESTS: {quest_count}"
                        f"\nINCOMPLETE QUESTS: {quest_count}"
                        f"\nCOMPLETE QUESTS: {completed_count}")
        side_panel_text.insert(END, updated_info)
    else:
        side_panel_text.delete("1.0", END)
        updated_info = (f"TOTAL QUESTS: 0"
                        f"\nINCOMPLETE QUESTS: 0"
                        f"\nCOMPLETE QUESTS: 0")
        side_panel_text.insert(END, updated_info)

def update_quest_history(quest, quest_history_listbox):
    quest_history_listbox.insert(END, quest)