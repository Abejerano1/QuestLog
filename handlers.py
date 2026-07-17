import quest
import ui

##### EVENT HANDLERS #####
def add_button_handler(current_user, entry_field, refresh_callback, database_connection, quest_lookup):
    """
    Handles quest addition button procedure.
    :param current_user: The current user.
    :param entry_field: The selected quest.
    :param refresh_callback: The function we are passing back
                             to refresh the list of quests.
    :param database_connection: The database connection.
    :return: None
    """
    print("Debug: Calling add_button_handler\n")
    # 1. Get the selected quest
    selection = entry_field.get()

    # Use the raw text string from the dropdown
    # as a key in the quest_lookup memory dictionary
    # ui.py: # Create dictionary to map selection to corresponding database entry
    #         quest_lookup = {quest.name: quest for quest in master_list}
    #
    #         # Create a list of only the quest names for UI purposes
    #         dropdown_options = list(quest_lookup.keys())
    selected_quest = quest_lookup.get(selection)

    # 2. Add quest
    # Package quest object
    new_quest = quest.Quest(id_num=selected_quest.get_id(),
                            name=selected_quest.get_name(),
                            exp=selected_quest.get_exp(),
                            desc=selected_quest.get_desc())
    # Create manager to access Quest functions
    manager = quest.QuestManager(database_connection)
    # Call add_quest()
    manager.add_quest(current_user.id_num, new_quest)

    # 3. Call refresh function
    refresh_callback(current_user)

    # 4. ui.update_side_pane()
    # ui.update_side_panel()

def del_button_handler(current_user, quest_listbox, refresh_callback, database_connection):
    """
    Handles quest deletion button procedure.
    :param current_user: The current user.
    :param quest_listbox: The quest listbox.
    :param refresh_callback: The function we are passing back
                             to refresh the list of quests.
    :param database_connection: The database connection.
    :return: None
    """
    # 1. Get the selected quest index from the listbox
    selection_index = quest_listbox.curselection()
    if not selection_index:
        print("DEBUG: No quest selected.")
    else:
        print(f"DEBUG: selection_index = {selection_index}")

    # Grab the selected row number
    chosen_row = selection_index[0]
    print(f"DEBUG: chosen_row = {chosen_row}")

    # Grab the full Quest object tied to the selected row
    target_quest = quest_listbox.active_quests[chosen_row]

    print(f"DEBUG: Quest name: {target_quest.name}")
    print(f"Entry ID: {target_quest.entry_id}")

    # 2. call quest.del_quest()
    # Create quest manager to access quest functions
    manager = quest.QuestManager(database_connection)

    #print("DEBUG: Calling del_button_handler\n")
    manager.del_quest(current_user.id_num, target_quest.get_entry_id())

    # 3. Call refresh function
    refresh_callback(current_user)

    # 4. Update side panel
    # ui.update_side_panel(side_panel_contents, quest_listbox, quest_history_listbox)

    # Update quest history listbox

def complete_button_handler(current_user,
                            quest_listbox,
                            quest_history_listbox,
                            refresh_callback,
                            history_refresh_callback,
                            database_connection):
    """
    Handles quest completion button procedure.
    :param current_user: The current user.
    :param quest_listbox: The quest listbox.
    :param refresh_callback: The function we are passing back
                             to refresh the list of quests.
    :param database_connection: The database connection.
    :return: None
    """
    # 1. Get the selected quest
    print("DEBUG: Getting selected quest...")
    selection_index = quest_listbox.curselection()
    # Isolate the name portion of the selection
    full_display_text = quest_listbox.get(selection_index[0])
    # Then, extract just the quest name by splitting at the separator
    quest_name = full_display_text.split(" - ")[0].strip()
    print(f"DEBUG: Quest name: {quest_name}")

    # 2. Call quest.set_complete()
    # Create quest manager to access quest functions
    manager = quest.QuestManager(database_connection)

    print("DEBUG: Calling complete_button_handler\n")
    manager.set_complete(current_user.id_num, quest_name)

    # 3. Call refresh function
    refresh_callback(current_user)
    # 4. Update side panel

    # 5. Update quest history panel
    history_refresh_callback(current_user, quest_history_listbox)
