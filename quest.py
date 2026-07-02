class Quest:
    id_num    : int = 1
    __next_id : int  = 1 # Class-level counter for unique IDs
    name      : str = None
    exp       : int = 0
    complete  : bool = False

    def __init__(self, id_num, name, desc, exp=10, complete=False):
        self.id_num = id_num
        self.name = name
        self.desc = desc
        self.exp = exp
        self.complete = complete

    def __int__(self) -> int:
        # Returns the quest id number
        return self.id_num

    def quest_exp(self) -> int:
        return self.exp

    def __str__(self) -> str:
        # Returns the quest name, description, and exp for listing purposes
        return f"{self.name}     {self.desc}     XP: {self.exp}"

    def complete_status(self) -> bool:
        # Returns the Boolean state for completion
        return self.complete

    def add_quest(quest, quest_history_listbox):
        """
        Add a quest to the listbox and commit changes to user's quest list
        :param quest_history_listbox:
        :return:
        """
        return

    def complete_quest(quest_listbox, side_panel_contents, quest_history_listbox):
        # Selects quest in listbox
        index = quest_listbox.curselection()
        # Updates quest completion status and commits changes to user's quest history
        index.complete = True
        # Debug print statement
        print(f"complete_quest - index: {index}")

        if not index:
            messagebox.showwarning(title="Warning!", message="You must select a quest!")
        else:
            # Gets the actual Quest object
            quest = quest_listbox.get(index)
            print(f"complete_quest - quest: {quest}")
            # Sends quest to history window
            add_quest_history(quest, quest_history_listbox)
            # Removes quest from main window
            del_quest(quest_listbox, side_panel_contents, quest_history_listbox)