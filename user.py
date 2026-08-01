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


    def get_id(self):
        """
        Function that returns user id
        :return: Int user id_num
        """
        return self.id_num


    def get_name(self):
        """
        Function that returns user's user_name
        :return: String of user's user_name
        """
        return self.user_name


    def get_level(self):
        """
        Function that returns user's user_level
        :return: Int of user's level
        """
        return self.level


    def get_exp(self):
        """
        Function that returns user's user_exp
        :return: Int of user's exp
        """
        return self.exp


    def get_user_class(self):
        """
        Function that returns user's user_class
        :return: String of user's user_class
        """
        return self.user_class


    def get_user_spec(self):
        """
        Function that returns user's user_spec
        :return: String of user's user_spec
        """
        return self.user_spec


    def get_complete_quests(self):
        """
        Function that returns user's complete_quests
        :return: Int of user's complete_quests
        """
        print("DEBUG: Running get_complete_quests()...")
        cursor = self.connection.cursor()

        try:
            print("DEBUG: Querying user info...")
            # 3. Execute simple single row query by ID
            query = f"""
                                SELECT complete_quests
                                FROM questlog.users
                                WHERE user_id = %s;
                            """
            cursor.execute(query, (self.id_num,))

            # 4. Store one row of data into user_info
            complete_quests = cursor.fetchone()

            # 5. Return the row of data
            print("DEBUG: User info successfully fetched!")
            print("DEBUG: Returning user info...")
            return complete_quests[0]

        except Error as e:
            print("Error while connecting to PostgreSQL", e)
            return None


    def get_incomplete_quests(self):
        """
        Function that returns user's incomplete_quests
        :return: Int of user's incomplete_quests
        """
        print("DEBUG: Running get_incomplete_quests()...")
        cursor = self.connection.cursor()

        try:
            print("DEBUG: Querying user info...")
            # 3. Execute simple single row query by ID
            query = f"""
                                        SELECT incomplete_quests
                                        FROM questlog.users
                                        WHERE user_id = %s;
                                    """
            cursor.execute(query, (self.id_num,))

            # 4. Store one row of data into user_info
            incomplete_quests = cursor.fetchone()

            # 5. Return the row of data
            print("DEBUG: User info successfully fetched!")
            print("DEBUG: Returning user info...")
            return incomplete_quests[0]

        except Error as e:
            print("Error while connecting to PostgreSQL", e)
            return None


    def get_total_quests(self):
        """
        Function that returns user's total_quests
        :return: Int of user's total_quests
        """
        print("DEBUG: Running get_total_quests()...")
        cursor = self.connection.cursor()

        try:
            print("DEBUG: Querying user info...")
            # 3. Execute simple single row query by ID
            query = f"""
                                        SELECT total_quests
                                        FROM questlog.users
                                        WHERE user_id = %s;
                                    """
            cursor.execute(query, (self.id_num,))

            # 4. Store one row of data into user_info
            total_quests = cursor.fetchone()

            # 5. Return the row of data
            print("DEBUG: User info successfully fetched!")
            print("DEBUG: Returning user info...")
            return total_quests[0]

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
                    completion_date=quest[4],
                    entry_id=quest[7]
                )

                result_quest_list.append(quest_object)

            return result_quest_list

        except Error as e:
            print("Error while connecting to PostgreSQL", e)
            return None


    def increment_total_quests(self):
        """
        Function that increments a User's "total_quests" count by 1
        :return: None
        """
        try:
            cursor = self.connection.cursor()

            # Execute update query
            query = f"""
                    UPDATE questlog.users
                    SET total_quests = total_quests + 1
                    WHERE user_id = %s;
            """
            cursor.execute(query, (self.id_num,))
            self.connection.commit()

        except Error as e:
            print("Error while running increment_total_quests", e)


    def increment_complete_quests(self):
        """
        Function that increments a User's "complete_quests" count by 1
        :return: None
        """
        try:
            cursor = self.connection.cursor()

            # Execute update query
            query = f"""
                    UPDATE questlog.users
                    SET complete_quests = complete_quests + 1
                    WHERE user_id = %s;
            """
            cursor.execute(query, (self.id_num,))
            self.connection.commit()

        except Error as e:
            print("Error while running increment_complete_quests", e)


    def decrement_incomplete_quests(self):
        """
        Function that decrements a User's "incomplete_quests" count by 1
        :return: None
        """
        try:
            cursor = self.connection.cursor()

            # Execute update query
            query = f"""
                    UPDATE questlog.users
                    SET incomplete_quests = incomplete_quests - 1
                    WHERE user_id = %s;
            """
            cursor.execute(query, (self.id_num,))
            self.connection.commit()

        except Error as e:
            print("Error while running decrement_incomplete_quests", e)