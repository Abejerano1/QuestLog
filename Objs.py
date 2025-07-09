import json

class Quest:
    _next_id = 1 # Class-level counter for unique IDs

    def __init__(self, name, exp=0):
        # Assign current unique ID
        self.id_num = Quest._next_id

        # Increment class-level counter for the next quest
        Quest._next_id += 1

        self.name = name
        self.exp = exp
        self.complete = False

    def __str__(self):
        # Returns the quest name and XP for listing purposes
        return f"{self.id_num}. {self.name}     XP: {self.exp}"

    def __int__(self):
        # Returns the quest id number
        return self.id_num

    def status_check(self):
        # Returns the Boolean state for completion
        return self.complete

    def to_dict(self):
        # Converts the Quest instance to a dictionary
        return {
            "quest_id": self.id_num,
            "name": self.name,
            "exp": self.exp,
            "complete": self.complete
        }