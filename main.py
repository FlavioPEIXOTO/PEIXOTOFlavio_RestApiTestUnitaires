from models import *
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Union
from typing import List
import sqlite3
from classes import *
from function import *


# Create a new sqlite database with tables
try:
    # Create database manager class
    databaseManager = DatabaseManager("pyRestApi.db")

    # Create table request queries for "users" and "games" table
    sqlite_create_table_users_query = '''CREATE TABLE users (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL UNIQUE,
                                password text NOT NULL);'''

    sqlite_create_table_games_query = '''CREATE TABLE games (id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL UNIQUE,
                                    description TEXT NULL,
                                    genre TEXT NULL,
                                    annee INT NULL,
                                    pegi INT NULL)'''

    # Calling database manager method to create table using previous queries
    databaseManager.create_sql_database(sqlite_create_table_games_query)
    databaseManager.create_sql_database(sqlite_create_table_users_query)


except sqlite3.Error as error:
    print("Error while creating a sqlite table", error)
finally:
    # Closing database connection
    if databaseManager.sqliteConnection:
        databaseManager.close_sql_connection()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Code": "201", "ServerResponse": "Welcome to GamingLibrary, an api rest to store games locally \n Also you can add users to manage too your game list"}


# Post route registering into db new users
@app.post("/register")
def register_user(logInformations: LogInformations):
    try:
        # Database connection
        databaseManager = DatabaseManager("pyRestApi.db")

        # Database select query, getting all users verifying if username already exist
        select_user_query = '''SELECT * FROM users WHERE username LIKE "{}"'''.format(
            logInformations.username)
        result = databaseManager.make_sql_request(select_user_query)

        if result is not None:
            return {"Code": "401", "Server Response": "Username already exist"}

        # Database insert a new user query
        sql_request = '''INSERT INTO users (username, password) VALUES ("{}", "{}");'''.format(
            logInformations.username, logInformations.password)
        databaseManager.make_sql_request(sql_request)

        # Close database connection
        databaseManager.close_sql_connection()

        return {"Code": "201", "Server Response": "User well registered"}

    except:
        print("Error encountered")
        raise Exception("An error has been encountered on user registration")


# Post route modifying username for an existing user
@app.post("/modifyUsername")
def modify_username(old_user_name: str, new_user_name: str):
    try:
        # Database connection
        databaseManager = DatabaseManager("pyRestApi.db")

        # Database select query, getting user by username
        select_user_query = '''SELECT * FROM users WHERE username LIKE "{}"'''.format(
            old_user_name)
        select_olduser_result = databaseManager.make_sql_request(
            select_user_query)

        if select_olduser_result is None:
            return {"Code": "401", "Server Response": "Cannot modify username, none user existing with username : " + old_user_name}

        sql_update_username_request = '''UPDATE users SET username = "{}" WHERE username LIKE "{}"'''.format(
            new_user_name, old_user_name)
        databaseManager.make_sql_request(sql_update_username_request)

        # Database select query, getting all users
        select_user_query = '''SELECT * FROM users WHERE username LIKE "{}"'''.format(
            old_user_name)
        select_user_result = databaseManager.make_sql_request(
            select_user_query)

        if select_user_result is not None:
            return {"Code": "401", "Server Response": "Username hasn't been modified"}

        # Close database connection
        databaseManager.close_sql_connection()

        return {"Code": "201", "Server Response": "Username well modified \n" + old_user_name + " => " + new_user_name}
    except:
        print("Error encountered")
        raise Exception("An error has been encountered modifying the username")

@app.get("/User")
def get_all_users():
    try:
        # Database connection
        databaseManager = DatabaseManager("pyRestApi.db")

        # Database select query, getting all users
        select_user_query = '''SELECT * FROM users'''
        result = databaseManager.make_sql_request(select_user_query)

        if result is not None:
            return {"Code": "201", "Server Response": result}
        else:
            return {"Code": "401", "Server Response": "None existing users"}
    except:
        print("Error encountered")
        raise Exception(
            "Error encountered when trying to get all existing users")


@app.put("/insertGame")
def insert_games(gameInformation: GameInformations):
    try:
        # Database connection
        databaseManager = DatabaseManager("pyRestApi.db")

        put_sql_query = '''INSERT INTO games (name, description, genre, annee, pegi) VALUES ("{}", "{}", "{}", {}, {})'''.format(
            gameInformation.name, gameInformation.description, gameInformation.genre, gameInformation.annee, gameInformation.pegi)
        result = databaseManager.make_sql_request(put_sql_query)

        databaseManager.close_sql_connection()

        if result != "Done":
            return {"Code": "401", "Server Response": "Cannot make insert games the request"}

        return {"Code": "201", "Server Response": "Game well added to game library"}
    except:
        print("Error encountered")
        raise Exception(
            "Error encountered when adding a game into games library")


@app.get("/myGames")
def get_my_games():
    try:
        # Database connection
        databaseManager = DatabaseManager("pyRestApi.db")

        # Database select query, getting all users
        select_game_query = "SELECT * FROM games"
        result = databaseManager.make_sql_request(select_game_query)

        if result is not None:
            return {"Code": "201", "Server Response": result}
        else:
            return {"Code": "401", "Server Response": "None existing games"}
    except:
        print("Error encountered")
        raise Exception(
            "Error encountered when getting all games from games library")

@app.delete("/deleteGame")
def delete_games(game_name):
    try:
        # Database connection
        databaseManager = DatabaseManager("pyRestApi.db")

        # Database select query, getting all users
        select_game_query = '''SELECT * FROM games WHERE name LIKE "{}"'''.format(
            game_name)
        result = databaseManager.make_sql_request(select_game_query)

        if result is None:
            return {"Code": "401", "Server Response": "None games in my library"}

        delete_game_query = '''DELETE FROM games WHERE name LIKE "{}"'''.format(
            game_name)
        result = databaseManager.make_sql_request(delete_game_query)

        if result != "Done":
            return {"Code": "401", "Server Response": "Cannot make delete games the request"}

        # Database select query, getting all users
        select_game_query = '''SELECT * FROM games WHERE name LIKE "{}"'''.format(
            game_name)
        result = databaseManager.make_sql_request(select_game_query)

        if result is not None:
            return {"Code": "401", "Server Response": "Game hasn't be deleted, check if game name is well write"}

        databaseManager.close_sql_connection()

        return {"Code": "201", "Server Response": "Game well delete to game library"}
    except:
        print("Error encountered")
        raise Exception(
            "Error encountered when trying to delete user  by username")
