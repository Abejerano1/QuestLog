#########################
# MAIN Tkinter BRANCH   #
#########################

#Start with a simple to-do list GUI

#Part 1: Create the GUI Elements
from tkinter import *
from tkinter import messagebox
from tkinter import ttk as tk
import lib as f

#Create root window
#Constructs Tk object named "root"
root = Tk()
root.title("Quest Log")

#root Configs:
root.configure(background="#cbc4c2")

#Set window width and height
window_width = 650
window_height = 600

#Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#Calculate position x, y to center the window
x = int(screen_width / 2 - window_width / 2)
y = int(screen_height / 2 - window_height / 2)

#Window dimensions
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

#Defines frame for containing our root window elements
base = tk.Frame(root, padding=10)
base.grid()

##### EVENT HANDLERS #####

def add_button_handler():
    quest = entry_field.get()
    if quest:
        f.add_task(quest_listbox, side_panel_text, quest)
        entry_field.delete(0, END)
    else:
        messagebox.showwarning(title="Warning!", message="You must enter a quest!")


def del_button_handler():
    f.del_task(quest_listbox, side_panel_text)

##### PLACEHOLDER TESTING DATA #####

player_level = 1
hp_points = 25
mana_points = 15
xp_points = 0


#Widgets displaying in root window
##### HEADER ICON #####
icon_section = tk.Label(base, text="Label1 - Icon",
          foreground="white",
          background="black")

icon_section.grid(column=0,
       row=0,
       sticky="w",
       padx=10,
       pady=15)

##### HEADER - USER STATS #####

user_header = tk.LabelFrame(base,
                            text="Label2 - User Header")

user_header.grid(row=0,
                 column=1,
                 sticky="w",
                 columnspan=2)

user_header_content = Text(user_header,
                           height=4,
                           width=10)

user_header_content.grid(column=2,
                         row=1,
                         columnspan=5,
                         rowspan=2)

header_data = ("LEVEL:" + f"{player_level}"
               "\nHP:" + f"{hp_points}"
               "\nMANA:" + f"{mana_points}"
               "\nEXP:" + f"{xp_points}")

user_header_content.insert(END, header_data)

##### MAIN WINDOW #####
main_window = tk.Label(base,
                       text="Label4 - Quest Window",
                       justify="left")

main_window.grid(column=1,
                 row=2,
                 sticky="w",
                 columnspan=2)

#Create Listbox
quest_listbox = Listbox(base,
                       height=10,
                       width=30,
                       bg="white",
                       fg="black",
                       selectmode=SINGLE,
                       activestyle="dotbox")

quest_listbox.grid(column=1,
                  row=2,
                  sticky="w")

##### USER STATS SIDEPANEL #####

#side panel
side_panel = tk.LabelFrame(base,
                           text="Statistics")

side_panel.grid(column=0,
                row=2,
                sticky="w")

side_panel_text = Text(side_panel,
                       width=25,
                       height=10)

side_panel_text.pack()


##### TASK OPTIONS #####
task_options = tk.Label(base,
         text="Label5 - Completed Tasks",
         justify="left")

task_options.grid(column=1,
                  row=3,
                  columnspan=2,
                  sticky="w")

#Section off our task options
task_options_container = tk.Frame(base)
task_options_container.grid(column=1,
                            row=4,
                            sticky="w")

##### ENTRY FIELD #####
entry_field = tk.Entry(task_options_container,
         justify="left")

entry_field.grid(column=1,
                 row=0)

#Submit entry on Enter keypress:
entry_field.bind("<Return>", lambda event: add_button_handler)

#Add entry button
add_button = tk.Button(task_options_container,
          text="Add quest",
          command=add_button_handler)

add_button.grid(column=0,
                row=0,
                sticky="w")

#Remove list entry
del_button = tk.Button(task_options_container,
                       text="Delete quest",
                       command=del_button_handler)

del_button.grid(column=0,
                row=1)

#Initialize item count
f.update_quest_count(quest_listbox, side_panel_text)

#Start the main events loop
root.mainloop()

