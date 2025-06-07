import json

class Quest:
    _next_id = 1 # Class-level counter for unique IDs

    def __init__(self, name, exp=0):

        self.id_num = Quest._next_id
        self.exp = exp
        self.name = name
        self.complete = False

    def __str__(self):
        return f"{self.name}     XP: {self.exp}"

    def status_check(self):
        # Returns:
        #   TRUE = complete
        #   FALSE = incomplete
        if self.complete:
            return True
        else:
            return False

user_profile_string = '''
{
    "username": "Grundel Sklanch",
    "id_num": "1",
    "level": "10",
    "exp": "200",
    "class": "Barbarian",
    "specialization": "Blacksmith"
}
'''

user_stats_string = '''
{
    "total_quests": <total_quests>,
    "completed": <completed>,
    "concurrent": <concurrent>,
    "abandoned": <abandoned>,
    "failed": <failed>,
    "Cumulative EXP": <accumulated EXP>
}
'''

def load_user_profile():
    return json.loads(user_profile_string)

def update_user_profile():
    pass