#!/usr/bin/python3
#
# author: a5892731
# version: 1.0
# date: 2021-06-17
# lat update: 2021-06-17
#
# Description:
# Ths is a script that creates a table in database
# It can be run directly from linux console
# ---------------------------------------------------------------------------------------------------------------------
#

try:
    import mysql.connector
    from mysql.connector import Error
except ImportError:
    print(">>> " + "No module: Install mysql.connector")

    import pip
    packages = [package.project_name for package in pip.get_installed_distributions()]
    if 'mysql.connector' not in packages:
        pip.main(['install', 'mysql.connector'])

class DBdata:  # <-------------------------------------------DATA FOR DATABASE------------------------------------------
    def __init__(self):
        self.db_name = "test_database"
        self.host_address = "127.0.0.1"
        self.user_name = "root"
        self.user_password = ""

        self.table_name = "test_table2"
        self.table_data = ("table_id INT AUTO_INCREMENT",
                           "column1 TEXT",
                           "column2 CHAR(30)",
                           "column3 INT")

        self.status = "" # class information status

        self.settings()

    def settings(self):
        user_choice = input(">>> >>> " + "Retrieve default settings (y/n/e)?: ")
        if user_choice.capitalize() == "Y":
            pass
        elif user_choice.capitalize() == "N":
            self.data_from_user()
        elif user_choice.capitalize() == "E":
            print(">>> " + "Exit program")
            exit()
        else:
            self.settings()

        self.status = "Database connection data collected"

    def data_from_user(self):

        self.db_name = input(">>> >>> " + "Input a database name: ")
        print(">>> " + "Your database name is {}".format(self.db_name))

        self.host_address = input(">>> >>> " + "Input a database address: ")
        print(">>> " + "Your database address is {}".format(self.host_address))

        self.user_name = input(">>> >>> " + "Input a user name: ")
        print(">>> " + "Your user name is {}".format(self.user_name))

        self.password_verify()

    def password_verify(self):
        password = input(">>> >>> " + "Input a user password: ")
        repeated_password = input(">>> >>> " + "Repeat a user password: ")

        if password == repeated_password:
            self.user_password = password
        else:
            print(">>> " + "Error! Try again")
            self.password_verify()

    def __del__(self):
        print(">>> " + "Connection data deleted")


class DatabaseConnector:
    def __init__(self, db_name, host_address, user_name, user_password):
        self.db_name = db_name
        self.host_address = host_address
        self.user_name = user_name
        self.user_password = user_password
        self.status = ""  # error status of DB
        self.connection = None

    def create_connection_to_server(self):

        try:
            self.connection = mysql.connector.connect(
                host=self.host_address,
                user=self.user_name,
                passwd=self.user_password,
                database=self.db_name
            )
            self.status = "Connection to MySQL server successful"
        except Error as e:
            self.status = f"The error '{e}' occurred"

    def execute_query(self, query, message):

        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            self.status = "{}".format(message)
        except Error as e:
            self.status = f"The error '{e}' occurred"



    def __del__(self):
        print(">>> " + "DB connector data deleted")


class TableBuilder:
    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table

        self.table_SQL = ""

    def create_table(self):

        def create_columns(table):
            columns = ""

            for column in table:
                columns += column + ", "
            columns += "PRIMARY KEY ({})".format(columns.split(" ")[0])

            return columns

        create_table = """
        CREATE TABLE IF NOT EXISTS {} (
          {}
        ) ENGINE = InnoDB 
        """.format(self.table_name, create_columns(self.table))

        #self.execute_query(self.connection, create_table, "DB {} table created successfully".format(self.table_name))

        self.table_SQL = create_table


    def __del__(self):
        print(">>> " + "Table builder data deleted")

#-----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    user_data = DBdata()

    connector = DatabaseConnector(user_data.db_name, user_data.host_address,
                                  user_data.user_name, user_data.user_password)

    connector.create_connection_to_server()
    print(">>> " + connector.status)


    table = TableBuilder(user_data.table_name, user_data.table_data)
    table.create_table()
    print("SQL: " + table.table_SQL)


    connector.execute_query(table.table_SQL,
                            "DB {} table created successfully".format(user_data.table_name))
    print(">>> " + connector.status)


