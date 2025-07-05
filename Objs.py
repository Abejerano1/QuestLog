import json

class Quest:
    _next_id = 1 # Class-level counter for unique IDs

    def __init__(self, name, exp=0):

        self.id_num = Quest._next_id
        self.name = name
        self.exp = exp
        self.complete = False

    def __str__(self):
        # Returns the quest name and XP for listing purposes
        return f"{self.name}     XP: {self.exp}"

    def __int__(self):
        # Returns the id quest id number
        return self.id_num

    def status_check(self):
        # Returns the Boolean state for completion
        return self.complete

    def to_dict(self):
        # Converts the Quest instance to a dictionary
        return {
            "id_num": self.id_num,
            "name": self.name,
            "exp": self.exp,
            "complete": self.complete
        }