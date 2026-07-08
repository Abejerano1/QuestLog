from multiprocessing import connection

import psycopg2
from psycopg2 import Error
from psycopg2 import sql

class Quest:
    def __init__(self, id_num=-1, name=None, desc=None, exp=10, complete=False, completion_date=None):
        self.id_num = id_num
        self.name = name
        self.exp = exp
        self.complete = complete
        self.completion_date = completion_date
        self.desc = desc

    def __int__(self) -> int:
        # Returns the quest id number
        return self.id_num

    def __str__(self) -> str:
        # Returns the quest name, description, and exp for listing purposes
        return f"{self.name}     {self.desc}     EXP: {self.exp}"

    def get_id(self) -> int:
        """
        Returns the id of the calling Quest object
        :return: Int Quest object id_num attribute
        """
        return self.id_num


    def get_name(self) -> str:
        """
        Returns the name of the calling Quest object
        :return: String Quest object name attribute
        """
        return self.name


    def get_desc(self) -> str:
        """
        Returns the description of the calling Quest object
        :return: String Quest object quest_description attribute
        """
        return self.desc


    def get_quest_exp(self) -> int:
        """
        Returns the exp of the calling Quest object
        :return: Integer Quest object exp attribute
        """
        return self.exp


    def get_complete_status(self) -> bool:
        """
        Returns the completion status of the calling Quest object
        :return: Boolean
        """
        return self.complete

class QuestManager:
    def __init__(self):
        """
        Initialize the manager and establish a single
        persistent connection.
        """
        try:
            # Connect to the database
            print("Connecting to database...")
            self.connection = psycopg2.connect(
                user="postgres",
                password="password",
                host="localhost",
                database="questlog",
                port="5432")
            print("Database connected!")

        except Error as e:
            print("Error while connecting to PostgreSQL", e)
            self.connection = None

    def close(self):
        """
        Function that safely closes the connection
        when the application closes.
        """
        if self.connection:
            print("Closing connection...")
            self.connection.close()
            print("Database connection closed safely.")

    def get_all_quests(self):
        """
        Returns a list of all quests
        :return: A list of all quests
        """
        if not self.connection:
            return

        # Create an array to store quest list
        result_quest_list = []

        print("DEBUG: Getting all quests...")
        try:
            # 1. Create a new cursor object
            cursor = self.connection.cursor()

            # 3. Execute simple single row query by ID
            query = f"""
                        SELECT *
                        FROM questlog.quests;
                    """
            cursor.execute(query)

            # Fetch every item in the master quest list
            quest_list = cursor.fetchall()
            for quest in quest_list:
                # Turn each database row into a Python Quest object
                quest_object = Quest(
                    id_num=quest[0],
                    name=quest[1],
                    desc=quest[2],
                    exp=quest[3]
                )
                # Append the quest object to the end of the list
                result_quest_list.append(quest_object)

            return result_quest_list

        except Error as e:
            print("Error while connecting to PostgreSQL", e)
            return None


    def add_quest(self, user_id, quest_name):
        """
        Commit a quest to the user's quest database
        :param quest_name: Name of the quest
        :return: None
        """
        print("DEBUG: Entered quest.add_quest.")
        if not self.connection:
            return

        # Case: Check if valid quest was selected before SQL query
        if not quest_name or quest_name in ["Select quest...", "No quests selected."]:
            print("ERROR: No valid quest selected.")
            return

        try:
            # Create a new cursor object
            cursor = self.connection.cursor()

            print(f"DEBUG: table_name = u_{user_id}_quests")
            table_name = f"u_{user_id}_quests"

            print("DEBUG: Executing query...")
            query = sql.SQL("""
                        INSERT INTO questlog.{table} (quest_name, quest_exp, quest_status, quest_id)
                        SELECT quest_name, quest_exp, 'INCOMPLETE', quest_id
                        FROM questlog.quests
                        WHERE quest_name = %s;
                    """).format(table=sql.Identifier(table_name))
            cursor.execute(query, (quest_name,))

            print("Query executed!")
            # Commit changes
            self.connection.commit()

            # Clean up connections
            cursor.close()
            print("DEBUG: Quest successfully added!")

        except Error as e:
            print("Error while connecting to PostgreSQL", e)


    def del_quest(self, user_id, quest_name):
        """
            Delete a quest from the user's quest database
            :param user_id: ID number of the current user.
            :param quest_name: Name of the quest.
            :return: None
        """

        # DEBUG
        print("DEBUG: Entered quest.del_quest.")

        # Case: Check if valid quest was selected before SQL query
        if not quest_name:
            print("ERROR: No valid quest selected.")
            return

        try:
            cursor = self.connection.cursor()

            table_name = f"u_{user_id}_quests"
            print(f"DEBUG: table_name = {table_name}")

            print("DEBUG: Executing query...")
            query = sql.SQL("""
                                DELETE FROM questlog.{table}
                                WHERE quest_name = %s;
                            """).format(table=sql.Identifier(table_name))
            cursor.execute(query, (quest_name,))

            print("DEBUG: Query executed!")
            # Commit changes
            self.connection.commit()
            # Clean up connections
            cursor.close()

            print(f"DEBUG: Quest {quest_name} successfully deleted!")
            print("DEBUG: Exiting quest.del_quest...")

        except Error as e:
            print("Error while connecting to PostgreSQL", e)


    def set_complete(self, user_id, quest_name):
        """
        Updates a quest's completion status to 'COMPLETE'
        :param side_panel_contents: TBD
        :param quest_history_listbox: TBD
        :return: None
        """
        if not quest_name:
            print("ERROR: No valid quest selected.")
            return

        try:
            cursor = self.connection.cursor()

            table_name = f"u_{user_id}_quests"
            print(f"DEBUG: table_name = {table_name}")

            print("DEBUG: Executing query...")
            query = sql.SQL("""
                UPDATE questlog.{table}
                set quest_status = 'COMPLETE'
                WHERE quest_name = %s;
                """).format(table=sql.Identifier(table_name))
            cursor.execute(query, (quest_name,))

            print("DEBUG: Query executed!")

            # Commit changes
            self.connection.commit()
            # Clean up
            cursor.close()

            print(f"DEBUG: Quest {quest_name} successfully updated!")
            print("DEBUG: Exiting quest.set_complete...")

        except Error as e:
            print("Error while connecting to PostgreSQL", e)
