#########################
# MAIN Tkinter BRANCH   #
#########################
import tkinter
#Start with a simple to-do list GUI

##### IMPORT STATEMENTS #####
from tkinter import *
from tkinter import ttk as tk
from tkinter import font
from PIL import Image, ImageTk
import lib as f

##### PLACEHOLDER TESTING DATA #####

username = "username"
player_level = "level"
exp = "exp"
user_class = "class"
user_specialization = "specialization"

#Loads placeholder data from user_profile JSON
username_result = f.get_attribute(username)
player_level_result = f.get_attribute(player_level)
exp_result = f.get_attribute(exp)
user_class_result = f.get_attribute(user_class)
user_specialization_result = f.get_attribute(user_specialization)

#Create root window
#Constructs Tk object named "root"
root = Tk()
root.title("Quest Log")

#root Configs:
root.configure(background="#0c1105")

#Set window width and height
window_width = 650
window_height = 800

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

##### GLOBAL COUNTERS #####

##### EVENT HANDLERS #####
def add_button_handler():
    f.add_quest(entry_field, quest_listbox, side_panel_contents, quest_history_listbox)
    f.update_side_panel(side_panel_contents, quest_listbox, quest_history_listbox)

def del_button_handler():
    #print("Debug: side_panel_text =", side_panel_text)
    f.del_quest(quest_listbox, side_panel_contents, quest_history_listbox)
    f.update_side_panel(side_panel_contents, quest_listbox, quest_history_listbox)


def complete_button_handler():
    #print("Debug: side_panel_text =", side_panel_text)
    f.complete_quest(quest_listbox, side_panel_contents,
                     quest_history_listbox, entry_field)
    f.update_side_panel(side_panel_contents, quest_listbox, quest_history_listbox)

#Widgets displaying in root window

##### HEADER ICON #####
icon_section = tk.LabelFrame(base,
                             text="User Icon")

icon_section.grid(column=0,
                  row=0)

icon_path = "Plankton_Meme.jpg"
icon = Image.open(icon_path)

preferred_width = 100
preferred_height = 100
resized_icon = icon.resize((preferred_width, preferred_height))

profile_icon = ImageTk.PhotoImage(resized_icon)
icon_panel = tkinter.Label(icon_section, image = profile_icon)
icon_panel.pack(fill = "both", expand = False)

##### HEADER - USER STATS #####

user_header = tk.LabelFrame(base,
                            text="User Header")

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
                           bg="black",
                           highlightcolor="#7fd900",
                           highlightbackground="#293b10",
                           highlightthickness=1)

user_header_content.pack(side="left")

header_data = (f"{username_result}"
                       "\nLEVEL: " + f"{player_level_result}"
                       "\nEXP: " + f"{exp_result}"
                       "\nCLASS: " + f"{user_class_result} - {user_specialization_result}")

user_header_content.insert(END, header_data)

##### MAIN WINDOW #####
main_window = tk.Labelframe(base,
                       text="Quest Log")

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
                        bg="black",
                        highlightcolor="#7fd900",
                        highlightbackground="#344b15",
                        highlightthickness=1)

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

side_panel_font = font.Font(family="Modeseven", size=10)

side_panel_contents = Listbox(side_panel,
                              width=20,
                              height=12,
                              font=side_panel_font,
                              fg="#7fd900",
                              bg="black",
                              highlightcolor="#7fd900",
                              highlightbackground="#293b10",
                              highlightthickness=1)

side_panel_contents.pack()



##### TASK OPTIONS #####
quest_options_container = tk.Labelframe(base,
                                        text="Task Options")
quest_options_container.grid(column=1,
                             row=4,
                             sticky="e",
                             pady=4)

##### ENTRY FIELD #####
entry_field_font = font.Font(family="Modeseven", size=10)

entry_field = tk.Entry(quest_options_container,
                       justify="left",
                       font=entry_field_font)

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

history_font = font.Font(family="Modeseven", size=10)

quest_history_listbox = Listbox(quest_history_panel,
                                width=60,
                                height=5,
                                selectmode="",
                                activestyle="dotbox",
                                font=history_font,
                                fg="#7fd900",
                                bg="black",
                                highlightcolor="#7fd900",
                                highlightbackground="#293b10",
                                highlightthickness=1)
quest_history_listbox.pack()



#Initialize side panel
f.initialize_side_panel(side_panel_contents)

#Start the main events loop
root.mainloop()