import datetime
import handlers as h
import psycopg2
import tkinter as tk
import user
from PIL import Image as PILImage, ImageTk
from tkinter import *
from tkinter import font
from psycopg2 import Error

class questlog_view:
    def __init__(self, root_window, database_connection):
        # Creates the root window
        self.root = root_window
        self.database_connection = database_connection

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

    def build(self):
        ##### PLACEHOLDER TESTING DATA #####

        # FETCH CURRENT USER DATA
        current_user = user.User(1, "Merlin", 28, 9001, "Mage", "Technomancer")
        user_info = current_user.get_info()

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

            user_id = user_idnum
            user_name = user_name
            user_level = user_level
            user_exp = user_exp
            user_class = user_class
            user_spec = user_spec


        # ===============================================

        # FETCH TIME & DATE
        current_time = datetime.datetime.now()
        current_date = f"{current_time.month}/{current_time.day}/{current_time.year}"
        # Menu Bar

        ##### QUEST LIST STORAGE ####
        quest_list = []
        completed_list = []

        #Widgets displaying in root window

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
        print(f"Loading user icon from {icon_path}...")


        icon = PILImage.open(icon_path)
        if icon:
            print("Loaded user icon.")
        else:
            print("Failed to load user icon.")

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
                                      highlightthickness=0)

        side_panel_contents.pack()

        # Initializes the stats panel with default values
        def initialize_side_panel(complete_quests, incomplete_quests, total_quests, side_panel_contents):
            side_panel_contents.insert(END, f"INCOMPLETE QUESTS: {incomplete_quests}")
            side_panel_contents.insert(END, f"COMPLETE QUESTS: {complete_quests}")
            side_panel_contents.insert(END, f"TOTAL QUESTS: {total_quests}")

        initialize_side_panel(complete_quests, incomplete_quests, total_quests, side_panel_contents)


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

        ##### ENTRY FIELD #####
        entry_field_font = font.Font(family="Modeseven", size=10)

        entry_field = Entry(quest_options_container,
                            justify="left",
                            font=entry_field_font,
                            bg="black",
                            fg="#63cbee",
                            insertbackground="#7fd900",
                            highlightthickness=0)

        entry_field.grid(column=1,
                         row=0,
                         padx=5)

        #Submit entry on Enter keypress:
        entry_field.bind("<Return>", lambda event: h.add_button_handler)

        ##### ADD ENTRY BUTTON #####
        add_button = Button(quest_options_container,
                            text="Add quest",
                            font=("Modeseven", 10),
                            fg="#7fd900",
                            bg="black",
                            highlightthickness=0,
                            command=h.add_button_handler,
                            width=10,
                            bd=0)

        add_button.grid(column=0,
                        row=0,
                        sticky="w")

        ##### DELETE ENTRY BUTTON #####
        del_button = Button(quest_options_container,
                            text="Delete quest",
                            font=("Modeseven", 10),
                            fg="#7fd900",
                            bg="black",
                            highlightthickness=0,
                            command=h.del_button_handler,
                            width=10,
                            bd=0)

        del_button.grid(column=0,
                        row=1,
                        sticky="w")

        ##### MARK COMPLETE BUTTON #####
        complete_button = Button(quest_options_container,
                                 text="Mark Complete",
                                 font=("Modeseven", 10),
                                 fg="#7fd900",
                                 bg="black",
                                 highlightthickness=0,
                                 command=h.complete_button_handler,
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
                                        highlightthickness=0)
        quest_history_listbox.pack()