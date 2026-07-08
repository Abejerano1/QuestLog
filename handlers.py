import quest
import ui


##### EVENT HANDLERS #####
def add_button_handler(current_user, entry_field, refresh_callback):
    """
    Handles quest addition button procedure.
    :param current_user: The current user.
    :param entry_field: The selected quest.
    :param refresh_callback: The function we are passing back
                             to refresh the list of quests.
    :return: None
    """
    print("Debug: Calling add_button_handler\n")
    # 1. Get the selected quest
    selection = entry_field.get()

    # 2. Add quest
    manager = quest.QuestManager()
    manager.add_quest(current_user.id_num, selection)

    # 3. Call refresh function
    refresh_callback(current_user)

    # 4. ui.update_side_pane()
    # ui.update_side_panel()

def del_button_handler(current_user, quest_listbox, refresh_callback):
    """
    Handles quest deletion button procedure.
    :param current_user: The current user.
    :param quest_listbox: The quest listbox.
    :param refresh_callback: The function we are passing back
                             to refresh the list of quests.
    :return: None
    """
    # 1. Get the selected quest index from the listbox
    selection_index = quest_listbox.curselection()
    # Isolate the name portion of the selection
    full_display_text = quest_listbox.get(selection_index[0])
    # Then, extract just the quest name by splitting at the separator
    quest_name = full_display_text.split(" - ")[0].strip()
    print(f"Quest name: {quest_name}")

    # 2. call quest.del_quest()
    # Create quest manager to access quest functions
    manager = quest.QuestManager()

    print("Debug: Calling del_button_handler\n")
    manager.del_quest(current_user.id_num, quest_name)

    # 3. Call refresh function
    refresh_callback(current_user)

    # 4. Update side panel
    # ui.update_side_panel(side_panel_contents, quest_listbox, quest_history_listbox)

    # Update quest history listbox

def complete_button_handler():
    """
    Handles quest completion button procedure.
    :return: None
    """
    # 1. Get the selected quest
    # something something.get

    #print("Debug: side_panel_text =", side_panel_text)
    quest.set_complete(quest_listbox, side_panel_contents,
                     quest_history_listbox)
    # 2. Update side panel
    # ui.update_side_panel(side_panel_contents, quest_listbox, quest_history_listbox)

    # 3. Update quest history
    # ui.update_quest_history