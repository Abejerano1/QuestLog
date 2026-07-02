#import psycopg2
import psycopg2
from psycopg2 import Error
from quest import Quest

class User:
    def __init__(self, id_num=0, username="User", level=1, exp=0,
                 user_class="Novice",
                 user_spec="Unemployed",
                 complete_quests=0,
                 incomplete_quests=0,
                 total_quests=0):
        self.id_num = id_num
        self.user_name = username
        self.level = level
        self.exp = exp
        self.user_class = user_class
        self.user_spec = user_spec
        self.complete_quests = complete_quests
        self.incomplete_quests = incomplete_quests
        self.total_quests = total_quests

    def get_info(self):
        try:
            # 1. Connect to the database
            connection = psycopg2.connect(
                user="postgres",
                password="password",
                host="localhost",
                database="questlog",
                port="5432")

            # 2. Create a new cursor object
            cursor = connection.cursor()

            # 3. Execute simple single row query by ID
            query = f"""
                        SELECT *
                        FROM questlog.users
                        WHERE user_id = {self.id_num};
                    """
            cursor.execute(query)
            user_info = cursor.fetchone()
            return user_info

        except Error as e:
            print("Error while connecting to PostgreSQL", e)
            return None

        finally:
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


    def get_quests(self, status):
        # Create an array to store quest list
        result_quest_list = []

        print(f"Getting {self.user_name}'s quests...")
        try:
            # 1. Connect to the database
            connection = psycopg2.connect(
                user="postgres",
                password="password",
                host="localhost",
                database="questlog",
                port="5432")

            # 2. Create a new cursor object
            cursor = connection.cursor()

            # 3. Execute simple single row query by ID
            query = f"""
                        SELECT *
                        FROM questlog.u_{self.user_name}_quests
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

        finally:
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")