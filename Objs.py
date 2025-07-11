import json

class Quest:
    __next_id : int  = 1 # Class-level counter for unique IDs
    id_num    : int = 1
    name      : str = None
    exp       : int = 0
    complete  : bool = False

    def __init__(self, name, exp=0):

        self.id_num = Quest._next_id
        self.name = name
        self.exp = exp
        self.complete = False

    def __str__(self) -> str:
        # Returns the quest name and XP for listing purposes
        return f"{self.name}     XP: {self.exp}"

    def __int__(self) -> int:
        # Returns the id quest id number
        return self.id_num

    def is_complete(self) -> bool:
        # Returns the Boolean state for completion
        return self.complete

    #def to_dict(self):
    #    # Converts the Quest instance to a dictionary
    #    return {
    #        "id_num": self.id_num,
    #        "name": self.name,
    #        "exp": self.exp,
    #        "complete": self.complete
    #    }
    
