class Quest:
    _next_id = 1 # Class-level counter for unique IDs

    def __init__(self, name, exp=0):
        self.id = Quest._next_id
        Quest._next_id += 1
        self.exp = exp
        self.name = name
        self.complete = False

    def __str__(self):
        return f"{self.name}                                (XP: {self.exp})"

    def status_check(self):
        # Returns:
        #   TRUE = complete
        #   FALSE = incomplete
        if self.complete:
            return True
        else:
            return False