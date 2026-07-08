from psycopg2 import sql
from psycopg2 import Error
from quest import Quest

class User:
    def __init__(self, id_num=0, username="User", level=1, exp=0,
                 user_class="Novice",
                 user_spec="Unemployed",
                 complete_quests=0,
                 incomplete_quests=0,
                 total_quests=0,
                 database_connection=None):

        self.id_num = id_num
        self.user_name = username
        self.level = level
        self.exp = exp
        self.user_class = user_class
        self.user_spec = user_spec
        self.complete_quests = complete_quests
        self.incomplete_quests = incomplete_quests
        self.total_quests = total_quests
        self.connection = database_connection

    def get_info(self):
        """
        Function that returns all info about a User
        :return: User object
        """
        print("DEBUG: Running user.get_info...")
        cursor = self.connection.cursor()

        try:
            print("DEBUG: Querying user info...")
            # 3. Execute simple single row query by ID
            query = f"""
                        SELECT *
                        FROM questlog.users
                        WHERE user_id = %s;
                    """
            cursor.execute(query, (self.id_num,))

            # 4. Store one row of data into user_info
            user_info = cursor.fetchone()

            # 5. Return the row of data
            print("DEBUG: User info successfully fetched!")
            print("DEBUG: Returning user info...")
            return user_info

        except Error as e:
            print("Error while connecting to PostgreSQL", e)
            return None



    def get_quests(self, status):
        """
        Function that returns all quests belonging to a User
        :param status: 'INCOMPLETE'/'COMPLETE'
        :return: List of quests
        """
        # Create an array to store quest list
        result_quest_list = []

        print(f"Getting {self.user_name}'s quests...")
        try:
            cursor = self.connection.cursor()

            # 3. Execute simple single row query by ID
            query = f"""
                        SELECT *
                        FROM questlog.u_{self.id_num}_quests
                        WHERE quest_status = %s;
                    """
            cursor.execute(query, (status,))

            user_quest_list = cursor.fetchall()
            for quest in user_quest_list:
                # Turn each database row into a Python Quest object
                quest_object = Quest(
                    name=quest[0],
                    exp=quest[1],
                    complete=quest[2],
                    id_num=quest[3],
                    completion_date=quest[4]
                )

                result_quest_list.append(quest_object)

            return result_quest_list

        except Error as e:
            print("Error while connecting to PostgreSQL", e)
            return None