import datetime
import tkinter as tk

import quest
from PIL import Image as PILImage, ImageTk
from tkinter import *
from tkinter import font
from tkinter import ttk


class questlog_view:
    def __init__(self, root_window, db_connection):
        """
        questlog_view class constructor
        :param root_window: The window within which the GUI will exist.
        :param database_connection: The database from which all data will be manipulated.
        """
        # Creates the root window
        self.root = root_window
        self.database_connection = db_connection

        # Configure window passed from main
        self.window_setup()

        # Defines window frame creation
        self.base = Frame(self.root,
                     bg="black",
                     padx=10,
                     pady=10)

        self.base.place(relx=0.5,
                        rely=0.5,
                        anchor="center")

    def window_setup(self):
        """
        Function that configures the main program window.
        :return: None
        """
        # Centers and sizes the main window
        self.root.title("Quest Log")
        self.root.configure(background = "black")

        # Set window width and height
        window_width = 650
        window_height = 800

        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate position x, y to center the window
        x = int(screen_width / 2 - window_width / 2)
        y = int(screen_height / 2 - window_height / 2)

        # Window dimensions
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")


    def build(self, current_user):
        """
        Function that builds the main program window.
        :return: None
        """
        # Import handlers
        import handlers as h
        # FETCH CURRENT USER DATA
        user_info = current_user.get_info()

        # If user info exists, assign it to variable user_info
        if user_info:
            (user_idnum,
             user_name,
             user_level,
             user_exp,
             user_class,
             user_spec,
             complete_quests,
             incomplete_quests,
             total_quests) = user_info

            # Assign variables for user attributes
            # (It may be better to use accessors instead later on)
            user_id = user_idnum
            user_name = user_name
            user_level = user_level
            user_exp = user_exp
            user_class = user_class
            user_spec = user_spec
            complete_quests = complete_quests
            incomplete_quests = incomplete_quests
            total_quests = total_quests

        # Create a QuestManager object to handle quest fetching
        quest_manager = quest.QuestManager(self.database_connection)

        # Fetch master list of quests
        master_list = quest_manager.get_all_quests()

        # Create dictionary to map selection to corresponding database entry
        quest_lookup = {quest.name: quest for quest in master_list}

        # Create a list of only the quest names for UI purposes
        dropdown_options = list(quest_lookup.keys())

        # FETCH TIME & DATE
        current_time = datetime.datetime.now()
        current_date = f"{current_time.month}/{current_time.day}/{current_time.year}"

        # ===============================================

        # Menu Bar

        # Populates the main quest listbox with current user's quests
        def populate_quest_log(current_user):
            """
            Function that populates the central quest log listbox.
            :param current_user: User object passed for their corresponding quest log
            :return: None
            """
            # DEBUG PRINT STATEMENT
            print("DEBUG: Running initialize_quest_listbox()...")

            # Clear out the old data to prevent compounding on refresh
            quest_listbox.delete(0, END)
            quest_listbox.active_quests = []

            # Retrieve all of current user's incomplete quests
            current_active_quests = current_user.get_quests("INCOMPLETE")
            # Insert quest entry into the end of the quest log listbox
            for quest in current_active_quests:
                list_item = f"{quest.name} - EXP: {quest.exp}"
                quest_listbox.insert(END, list_item)

                quest_listbox.active_quests.append(quest)

        def update_quest_log(current_user):
            """
            Function that refreshes (updates) the central quest log listbox.
            :param current_user: The list belonging to the current user that is being updated.
            :return: None
            """
            # DEBUG PRINT STATEMENT
            print("DEBUG: Running update_quest_listbox()...")

            # Clear listbox
            quest_listbox.delete(0, END)
            quest_listbox.active_quests = []

            # Assign the list of active quests into current_active_quests
            current_active_quests = current_user.get_quests("INCOMPLETE")

            # List for keeping track of the entry IDs
            quest_listbox.active_quests = []

            # Repopulate listbox
            for quest in current_active_quests:
                list_item = f"{quest.name} - EXP: {quest.exp}"
                quest_listbox.insert(END, list_item)

                # Track the unique entry ID
                quest_listbox.active_quests.append(quest)

            entry_field.set("Select quest...")

        # Initializes the 'COMPLETED QUESTS' list with completed quests
        def populate_quest_history(current_user):
            """
            Function that initializes a user's 'Completed Quests' list
            :param current_user: The list belonging to the current user that is being updated.
            """
            # DEBUG PRINT STATEMENT
            print("DEBUG: Running populate_quest_listbox()...")

            # Clear listbox
            print("Clearing quest_history_listbox...")
            quest_history_listbox.delete(0, END)

            # Declare list for tracking entry IDs
            quest_history_listbox.completed_quests = []

            # Fetch quests with status "COMPLETE"
            current_completed_quests = current_user.get_quests("COMPLETE")

            # Populate the listbox and the tracking list
            for quest in current_completed_quests:
                list_item = f"{quest.name} - {quest.complete}"
                quest_history_listbox.insert(END, list_item)

                quest_history_listbox.completed_quests.append(quest)

        def update_quest_history(current_user):
            """
            Function that updates the quest_history listbox at the
            foot of the main window.
            :param current_user: The quest history listbox of the currently
            active user.
            :return: None
            """
            # DEBUG PRINT STATEMENT
            print("DEBUG: Running update_quest_history()...")

            # Clear listbox
            quest_history_listbox.delete(0, END)

            # Declare list for tracking entry IDs
            quest_history_listbox.completed_quests = []

            # Assign the list of active quests into current_active_quests
            current_active_quests = current_user.get_quests("COMPLETE")

            # Repopulate listbox
            for quest in current_active_quests:
                list_item = f"{quest.name} - {quest.complete}"
                quest_history_listbox.insert(END, list_item)

                quest_history_listbox.completed_quests.append(quest)


        # Initializes the stats panel with default values
        def populate_side_panel(complete_quests, incomplete_quests, total_quests, side_panel_contents):
            """
            Function that populates the side statistics panel.
            :param complete_quests: Number of user's completed quests.
            :param incomplete_quests: Number of user's incomplete quests.
            :param total_quests: Number of all of user's quests.
            :param side_panel_contents: The side panel's listbox where the statistics
                    can be seen.
            :return: None
            """
            # Gather the variables
            incomplete_entry = (f"INCOMPLETE QUESTS: {incomplete_quests}")
            complete_entry = (f"COMPLETE QUESTS: {complete_quests}")
            total_entry = (f"TOTAL QUESTS: {total_quests}")

            # List them
            side_panel_contents.insert(END, incomplete_entry)
            side_panel_contents.insert(END, complete_entry)
            side_panel_contents.insert(END, total_entry)


        # Updates the stats panel with current values
        def update_side_panel(current_user):
            """
            Function that updates the side statistics panel.
            :param complete_quests: Number of user's completed quests.
            :param incomplete_quests: Number of user's incomplete quests.
            :param total_quests: Number of all of user's quests.
            :param side_panel_contents: The side panel's listbox where the statistics
                    can be seen.
            :return: None
            """
            print("DEBUG: Running update_side_panel()...")

            # Clear the side panel contents
            side_panel_contents.delete(0, END)

            # Gather the variables
            incomplete_entry = (f"INCOMPLETE QUESTS: {current_user.incomplete_quests}")
            complete_entry = (f"COMPLETE QUESTS: {current_user.complete_quests}")
            total_entry = (f"TOTAL QUESTS: {current_user.total_quests}")

            # List them
            side_panel_contents.insert(END, incomplete_entry)
            side_panel_contents.insert(END, complete_entry)
            side_panel_contents.insert(END, total_entry)


        # Widgets displaying in root window

        ##### HEADER ICON #####
        icon_section = LabelFrame(self.base,
                                  text=f"{user_name}",
                                  bg="black",
                                  fg="#63cbee",
                                  padx=10,
                                  pady=10,
                                  font=("Modeseven", 12, "bold"),
                                  highlightthickness=0,
                                  bd=0)

        icon_section.grid(column=0,
                          row=0)

        icon_path = "usermedia/1/test_wizard"

        # DEBUG
        print(f"DEBUG: Loading user icon from {icon_path}...")
        icon = PILImage.open(icon_path)
        if icon:
            print("DEBUG: Loaded user icon.")
        else:
            print("DEBUG: Failed to load user icon.")

        preferred_width = 100
        preferred_height = 100
        resized_icon = icon.resize((preferred_width, preferred_height))

        self.profile_icon = ImageTk.PhotoImage(resized_icon)

        icon_panel = tk.Label(icon_section, image=self.profile_icon, bg="black")
        icon_panel.pack(fill = "both", expand = False)

        ##### HEADER - USER INFO #####

        user_header = LabelFrame(self.base,
                                 text="User Header",
                                 bg="black",
                                 fg="#63cbee",
                                 font=("Modeseven", 12, "bold"),
                                 bd=0,
                                 relief="flat",
                                 takefocus=0)

        user_header.grid(row=0,
                         column=1,
                         columnspan=2,
                         sticky="w")

        header_font = font.Font(family="Modeseven", size=10)

        user_header_content = Text(user_header,
                                   height=4,
                                   width=40,
                                   font=header_font,
                                   fg="#7fd900",
                                   bg="#0c1105",
                                   highlightcolor="#7fd900",
                                   highlightbackground="#293b10",
                                   highlightthickness=0,
                                   takefocus=0)
        user_header_content.pack(side="left")

        header_data = (f"{current_date}"
                       "\nLEVEL: " + f"{user_level}"
                       "\nEXP: " + f"{user_exp}"
                       "\nCLASS: " + f"{user_class} - {user_spec}")

        user_header_content.insert(END, header_data)

        # Lock user header config into place
        user_header_content.config(state="disabled")

        ##### MAIN WINDOW #####
        main_window = LabelFrame(self.base,
                                 text="Quest Log",
                                 font=("Modeseven", 12, "bold"),
                                 fg="#63cbee",
                                 bg="black",
                                 highlightthickness=0,
                                 bd=0)

        main_window.grid(column=1,
                         row=2,
                         sticky="w",
                         columnspan=2)

        main_window_font = font.Font(family="Modeseven", size=10)

        quest_listbox = Listbox(main_window,
                                height=12,
                                width=40,
                                selectmode=SINGLE,
                                activestyle="dotbox",
                                font=main_window_font,
                                fg="#7fd900",
                                bg="#0c1105",
                                highlightcolor="#7fd900",
                                highlightbackground="#344b15",
                                highlightthickness=1)

        quest_listbox.grid(column=1,
                           row=2,
                           sticky="w")
        quest_listbox.yview()

        # List for the unique entry IDs
        quest_listbox.active_quests = []
        print(f"DEBUG: active_quests[]:")

        for item in quest_listbox.active_quests:
           print(f"DEBUG: {item}")

        print("DEBUG: Initializing quest_listbox...")
        # INITIALIZE QUEST_LISTBOX
        try:
            populate_quest_log(current_user)
            print("DEBUG: Initialized quest listbox.")
        except Exception as e:
            print(f"DEBUG: Failed to initialize quest listbox: {e}")


        ##### USER STATS SIDE PANEL #####

        #side panel
        side_panel = LabelFrame(self.base,
                                text="Statistics",
                                font=("Modeseven", 12, "bold"),
                                bg="black",
                                fg="#63cbee",
                                highlightthickness=0,
                                bd=0)

        side_panel.grid(column=0,
                        row=2,
                        sticky="w")

        side_panel_font = font.Font(family="Modeseven", size=10)

        side_panel_contents = Listbox(side_panel,
                                      width=20,
                                      height=12,
                                      font=side_panel_font,
                                      fg="#7fd900",
                                      bg="#0c1105",
                                      highlightcolor="#7fd900",
                                      highlightbackground="#293b10",
                                      highlightthickness=0,
                                      takefocus=0)

        side_panel_contents.pack()

        # INITIALIZE SIDE PANEL
        populate_side_panel(complete_quests, incomplete_quests, total_quests, side_panel_contents)

        # ==================================================================================================================== #

        ##### QUEST OPTIONS #####
        quest_options_container = LabelFrame(self.base,
                                             text="Task Options",
                                             font=("Modeseven", 12, "bold"),
                                             fg="#63cbee",
                                             bg="black",
                                             highlightthickness=0,
                                             padx=10)
        quest_options_container.grid(column=1,
                                     row=4,
                                     sticky="e",
                                     padx=5,
                                     pady=5)

        # ==================================================================================================================== #

        ##### QUEST ADDITION #####
        entry_field_font = font.Font(family="Modeseven", size=10)

        entry_field = ttk.Combobox(quest_options_container,
                                   justify="left",
                                   font=entry_field_font,
                                   state="readonly")

        entry_field.grid(column=1,
                         row=0,
                         padx=5)

        # Populate quest selection list
        entry_field['values'] = dropdown_options
        if (master_list):
            entry_field.set("Select quest...")
        else:
            entry_field.set("No quests selected.")

        ##### ADD ENTRY BUTTON #####
        add_button = Button(quest_options_container,
                            text="Add quest",
                            font=("Modeseven", 10),
                            fg="white",
                            bg="black",
                            highlightthickness=0,
                            command=lambda: h.add_button_handler(current_user,
                                                                 entry_field,
                                                                 update_quest_log,
                                                                 self.database_connection,
                                                                 quest_lookup),
                            width=10,
                            bd=0)

        add_button.grid(column=0,
                        row=0,
                        sticky="w")

        ##### DELETE ENTRY BUTTON #####
        del_button = Button(quest_options_container,
                            text="Delete quest",
                            font=("Modeseven", 10),
                            fg="white",
                            bg="black",
                            highlightthickness=0,
                            command=lambda: h.del_button_handler(current_user,
                                                                 quest_listbox,
                                                                 update_quest_log,
                                                                 self.database_connection),
                            width=10,
                            bd=0)

        del_button.grid(column=0,
                        row=1,
                        sticky="w")

        ##### MARK COMPLETE BUTTON #####
        complete_button = Button(quest_options_container,
                                 text="Mark Complete",
                                 font=("Modeseven", 10),
                                 fg="white",
                                 bg="black",
                                 highlightthickness=0,
                                 command=lambda: h.complete_button_handler(current_user,
                                                                           quest_listbox,
                                                                           quest_history_listbox,
                                                                           update_quest_log,
                                                                           update_quest_history,
                                                                           update_side_panel,
                                                                           self.database_connection),
                                 width=10,
                                 bd=0)

        complete_button.grid(column=0,
                             row=2,
                             sticky="w")

        ##### QUEST HISTORY FOOTER PANEL #####
        quest_history_panel = LabelFrame(self.base,
                                         text="Completed Quests:",
                                         bg="black",
                                         fg="#ffdb14",
                                         font=("Modeseven", 12, "bold"),
                                         bd=0,
                                         relief="flat",
                                         takefocus=0)

        quest_history_panel.grid(column=0,
                                 row = 5,
                                 columnspan=3,
                                 sticky="w",
                                 pady=5)

        history_font = font.Font(family="Modeseven", size=10)

        quest_history_listbox = Listbox(quest_history_panel,
                                        width=60,
                                        height=5,
                                        selectmode="",
                                        activestyle="dotbox",
                                        font=history_font,
                                        fg="#7fd900",
                                        bg="#0c1105",
                                        highlightcolor="#7fd900",
                                        highlightbackground="#293b10",
                                        highlightthickness=0,
                                        takefocus=0)
        quest_history_listbox.pack()

        # List for the unique entry IDs
        quest_history_listbox.completed_quests = []
        print(f"DEBUG: completed_quests[]:")

        for item in quest_history_listbox.completed_quests:
            print(f"DEBUG: {item}")

        print("DEBUG: Initializing quest_history_listbox...")
        # INITIALIZE QUEST_HISTORY_LISTBOX
        try:
            populate_quest_history(current_user)
            print("DEBUG: Initialized quest history listbox.")
        except Exception as e:
            print(f"DEBUG: Failed to initialize quest history listbox: {e}")