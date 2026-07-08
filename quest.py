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

class QuestManager:

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


    def get_all_quests(self):
        """
        Returns a list of all quests
        :return: A list of all quests
        """
        # Create an array to store quest list
        result_quest_list = []

        print("Getting all quests...")
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
        print("Entered quest.add_quest.")

        # Case: Check if valid quest was selected before SQL query
        if not quest_name or quest_name in ["Select quest...", "No quests selected."]:
            print("ERROR: No valid quest selected.")
            return

        try:
            print("Connecting to database...")
            # 1. Connect to the database
            connection = psycopg2.connect(
                user="postgres",
                password="password",
                host="localhost",
                database="questlog",
                port="5432")

            print("Database connected!")

            # 2. Create a new cursor object
            cursor = connection.cursor()

            print(f"table_name = u_{user_id}_quests")
            table_name = f"u_{user_id}_quests"

            print("Executing query...")
            query = sql.SQL("""
                        INSERT INTO questlog.{table} (quest_name, quest_exp, quest_status, quest_id)
                        SELECT quest_name, quest_exp, 'INCOMPLETE', quest_id
                        FROM questlog.quests
                        WHERE quest_name = %s;
                    """).format(table=sql.Identifier(table_name))
            cursor.execute(query, (quest_name,))

            print("Query executed!")
            # Commit changes
            connection.commit()

            # Clean up connections
            cursor.close()
            connection.close()
            print("Quest successfully added!")

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
        print("Entered quest.del_quest.")

        # Case: Check if valid quest was selected before SQL query
        if not quest_name:
            print("ERROR: No valid quest selected.")
            return

        try:
            print("Connecting to database...")
            # 1. Connect to the database
            connection = psycopg2.connect(
                user="postgres",
                password="password",
                host="localhost",
                database="questlog",
                port="5432")

            print("Database connected!")

            # 2. Create a new cursor object
            cursor = connection.cursor()

            print(f"table_name = u_{user_id}_quests")
            table_name = f"u_{user_id}_quests"

            print("Executing query...")
            query = sql.SQL("""
                                DELETE FROM questlog.{table}
                                WHERE quest_name = %s;
                            """).format(table=sql.Identifier(table_name))
            cursor.execute(query, (quest_name,))

            print("Query executed!")
            # Commit changes
            connection.commit()

            # Clean up connections
            cursor.close()
            connection.close()
            print("Quest successfully deleted!")
            print("Exiting quest.del_quest...")

        except Error as e:
            print("Error while connecting to PostgreSQL", e)


    def set_complete(quest_listbox, side_panel_contents, quest_history_listbox):
        """
        Updates a quest's completion status to 'COMPLETE'
        :param side_panel_contents: TBD
        :param quest_history_listbox: TBD
        :return: None
        """

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