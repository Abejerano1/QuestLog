

##### EVENT HANDLERS #####
def add_button_handler():
    f.add_quest(entry_field, quest_listbox, side_panel_contents, quest_history_listbox, "user1.json")
    f.update_side_panel(side_panel_contents, quest_listbox, quest_history_listbox)

def del_button_handler():
    #print("Debug: side_panel_text =", side_panel_text)
    f.del_quest(quest_listbox, side_panel_contents, quest_history_listbox)
    f.update_side_panel(side_panel_contents, quest_listbox, quest_history_listbox)

def complete_button_handler():
    #print("Debug: side_panel_text =", side_panel_text)
    f.complete_quest(quest_listbox, side_panel_contents,
                     quest_history_listbox)
    f.update_side_panel(side_panel_contents, quest_listbox, quest_history_listbox)