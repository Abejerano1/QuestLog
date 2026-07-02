#import psycopg2
import psycopg2
from psycopg2 import Error

class User:
    def __init__(self, id_num=0, username="User", level=1, exp=0,
                 user_class="Novice",
                 user_spec="Unemployed"):
        self.id_num = id_num
        self.username = username
        self.level = level
        self.exp = exp
        self.user_class = user_class
        self.user_spec = user_spec

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