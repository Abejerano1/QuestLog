#########################
# MAIN Tkinter BRANCH   #
#########################

#Start with a simple to-do list GUI

##### IMPORT STATEMENTS #####
from tkinter import *
from tkinter import ttk as tk
import lib as f

##### PLACEHOLDER TESTING DATA #####

player_level = 1
hp_points = 25
mana_points = 15
xp_points = 0

#Create root window
#Constructs Tk object named "root"
root = Tk()
root.title("Quest Log")

#root Configs:
root.configure(background="#cbc4c2")

#Set window width and height
window_width = 650
window_height = 750

#Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#Calculate position x, y to center the window
x = int(screen_width / 2 - window_width / 2)
y = int(screen_height / 2 - window_height / 2)

#Window dimensions
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

#Defines frame for containing our root window elements
base = tk.Frame(root,
                padding=10,)
base.place(relx=0.5,
           rely=0.5,
           anchor="center")

##### QUEST LIST STORAGE ####
quest_list = []
completed_list = []

##### EVENT HANDLERS #####
def add_button_handler():
    quest = entry_field.get()
    entry_field.delete(0, END)
    print("Debug: side_panel_text =", side_panel_text)
    f.add_quest(quest, quest_listbox, side_panel_text, quest_list)


def del_button_handler():
    #print("Debug: side_panel_text =", side_panel_text)
    f.del_quest(quest_listbox, side_panel_text, quest_list)


def complete_button_handler():
    #print("Debug: side_panel_text =", side_panel_text)
    f.complete_quest(quest_listbox, side_panel_text,
                     quest_history_listbox, quest_list, completed_list)

#Widgets displaying in root window

##### HEADER ICON #####
icon_section = tk.Label(base, text="Label1 - Icon",
                        foreground="white",
                        background="black",
                        justify="center")

icon_section.grid(column=0,
                  row=0,
                  ipadx=10,
                  ipady=10)

##### HEADER - USER STATS #####

user_header = tk.LabelFrame(base,
                            text="Label2 - User Header")

user_header.grid(row=0,
                 column=1,
                 sticky="w")

user_header_content = Text(user_header,
                           height=4,
                           width=10)

user_header_content.pack(side="left")

header_data = ("LEVEL:" + f"{player_level}"
               "\nHP:" + f"{hp_points}"
               "\nMANA:" + f"{mana_points}"
               "\nEXP:" + f"{xp_points}")

user_header_content.insert(END, header_data)

##### MAIN WINDOW #####
main_window = tk.Labelframe(base,
                       text="Quest Window")

main_window.grid(column=1,
                 row=2,
                 sticky="w",
                 columnspan=2)

#Create Listbox
quest_listbox = Listbox(main_window,
                        height=10,
                        width=40,
                        bg="white",
                        fg="black",
                        selectmode=SINGLE,
                        activestyle="dotbox")

quest_listbox.grid(column=1,
                  row=2,
                  sticky="w")
quest_listbox.yview()

##### USER STATS SIDEPANEL #####

#side panel
side_panel = tk.LabelFrame(base,
                           text="Statistics")

side_panel.grid(column=0,
                row=2,
                sticky="w")

side_panel_text = Text(side_panel,
                       width=20,
                       height=12)
side_panel_text.pack()



##### TASK OPTIONS #####
quest_options_container = tk.Labelframe(base,
                                        text="Task Options",
                                        padding=4)
quest_options_container.grid(column=1,
                             row=4,
                             sticky="w",
                             pady=4)

##### ENTRY FIELD #####
entry_field = tk.Entry(quest_options_container,
         justify="left")

entry_field.grid(column=1,
                 row=0,
                 padx=5)

#Submit entry on Enter keypress:
entry_field.bind("<Return>", lambda event: add_button_handler)

##### ADD ENTRY BUTTON #####
add_button = tk.Button(quest_options_container,
                        text="Add quest",
                        command=add_button_handler,
                        width=13)

add_button.grid(column=0,
                row=0,
                sticky="w")

##### DELETE ENTRY BUTTON #####
del_button = tk.Button(quest_options_container,
                       text="Delete quest",
                       command=del_button_handler,
                       width=13)

del_button.grid(column=0,
                row=1,
                sticky="w")

##### MARK COMPLETE BUTTON #####
complete_button = tk.Button(quest_options_container,
                            text="Mark Complete",
                            command=complete_button_handler,
                            width=13)

complete_button.grid(column=0,
                     row=2,
                     sticky="w")

##### QUEST HISTORY FOOTER PANEL #####
quest_history_panel = tk.Labelframe(base,
                                    text="Completed Quests:")

quest_history_panel.grid(column=0,
                         row = 5,
                         columnspan=3,
                         sticky="w",
                         pady=5)

quest_history_listbox = Listbox(quest_history_panel,
                                width=60,
                                height=5,
                                selectmode="",
                                activestyle="dotbox")
quest_history_listbox.pack()



#Initialize item count
f.update_side_panel(side_panel_text, quest_history_listbox, quest_listbox)

#Start the main events loop
root.mainloop()