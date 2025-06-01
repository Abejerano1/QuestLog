#########################
# MAIN Tkinter BRANCH   #
#########################

#Start with a simple to-do list GUI

#Part 1: Create the GUI Elements
from tkinter import *
from tkinter import ttk as tk
import lib as f

#Create root window
#Constructs Tk object named "root"
root = Tk()
root.title("Quest Log")

#root Configs:
root.configure(background="#cbc4c2")

#Window dimensions
root.geometry("500x600")

#Defines frame for containing our root window elements
base = tk.Frame(root, padding=10)
base.grid()

##### EVENT HANDLERS #####

def add_button_handler():
    quest = entry_field.get()
    if quest:
        f.add_task(quest_listbox, quest_counter_label, quest)
        entry_field.delete(0, END)

def del_button_handler():
    f.del_task(quest_listbox, quest_counter_label)

#Widgets displaying in root window
##### HEADER SECTION #####
icon_section = tk.Label(base, text="Label1 - Icon",
          foreground="white",
          background="black")

icon_section.grid(column=0,
       row=0,
       sticky="w",
       padx=10,
       pady=15)

user_header = tk.Label(base,
                       text="Label2 - User Header",
                       justify="left",
                       background="gray")

user_header.grid(column=1,
                 row=0,
                 sticky="w",
                 columnspan=2)

##### MAIN WINDOW #####
main_window = tk.Label(base,
                       text="Label4 - Quest Window",
                       justify="left")

main_window.grid(column=1,
                 row=1,
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
side_panel = tk.Frame(base)

side_panel.grid(column=0,
                row=2,
                sticky="w")

quest_counter_label = tk.Label(side_panel,
                              text="Total quests: 0")
quest_counter_label.pack()


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
f.update_quest_count(quest_listbox, quest_counter_label)

#Start the main events loop
root.mainloop()

