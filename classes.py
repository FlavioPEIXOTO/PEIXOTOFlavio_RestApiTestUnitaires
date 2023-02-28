import sqlite3
from function import *


class DatabaseManager():

    def __init__(self, databaseName):
        try:
            if isinstance(databaseName, str) and databaseName.endswith('.db'):
                self.databaseName = databaseName
            else:
                raise ValueError(
                    "Database name must be a string and end with .db extension")

            self.sqliteConnection = sqlite3.connect('pyRestApi.db')
            self.cursor = self.sqliteConnection.cursor()
        except:
            print("An error occured on instantiation of DatabaseManager")
            raise Exception("DatabaseManager initialization error")

    def create_sql_database(self, sqlite_create_table_request):
        try:
            print("Trying to create database table")
            self.cursor.execute(sqlite_create_table_request)
            self.sqliteConnection.commit()
            print("==> Database table well created")
        except:
            print("Table already exists or cannot be created")

    # Do sql request by giving sqlrequest string
    def make_sql_request(self, sqlite_request):
        try:
            request_type = get_sql_request_type_by_request_string(
                sqlite_request)
            print("Request type: " + request_type)
            print("SQL Request")
            self.cursor.execute(sqlite_request)
            self.sqliteConnection.commit()
            print("==> DONE")

            result = self.cursor.fetchall()

            if request_type == "SELECT":
                if (len(result) > 0):
                    print("User founded")
                    return result
                else:
                    print("None user founded")
                    return None
            else:
                return "Done"

        except:
            print("An error has occured when trying to do a request to sqlite database : {}".format(
                self.databaseName))
            raise Exception("Error occured on making sql request")

    def close_sql_connection(self):
        self.sqliteConnection.close()
        print("sqlite connection is closed")

    def delete_all_db_elements(self):
        delete_all_users_query = '''DELETE FROM users'''
        delete_all_games_query = '''DELETE FROM games'''

        self.cursor.execute(delete_all_users_query)
        self.sqliteConnection.commit()

        self.cursor.execute(delete_all_games_query)
        self.sqliteConnection.commit()


class ServerUser():

    def __init__(self):
        self.username = "None"
        self.loginStatus = True

    def user_login(self, username):
        if isinstance(username, str):
            self.username = username
        else:
            raise ValueError("Username not a string")

        if (self.loginStatus is False):
            self.loginStatus = True
            print("User well logged in")
            return self.loginStatus
        else:
            print("User already logged in")
            return False

    def user_disconnect(self):
        if (self.loginStatus is True):
            self.loginStatus = False
            print("User well disconnected")
            return self.loginStatus
        else:
            print("Cannot disconnect the user")
            return False

    def check_user_login(self):
        return self.loginStatus
