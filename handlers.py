import quest
import ui

##### EVENT HANDLERS #####
def add_button_handler():
    quest.add_quest(entry_field, quest_listbox, side_panel_contents, quest_history_listbox, "user1.json")
    # ui.update_side_panel(side_panel_contents, quest_listbox, quest_history_listbox)

def del_button_handler():
    #print("Debug: side_panel_text =", side_panel_text)
    quest.del_quest(quest_listbox, side_panel_contents, quest_history_listbox)
    # ui.update_side_panel(side_panel_contents, quest_listbox, quest_history_listbox)

def complete_button_handler():
    #print("Debug: side_panel_text =", side_panel_text)
    quest.set_complete(quest_listbox, side_panel_contents,
                     quest_history_listbox)
    # f.update_side_panel(side_panel_contents, quest_listbox, quest_history_listbox)