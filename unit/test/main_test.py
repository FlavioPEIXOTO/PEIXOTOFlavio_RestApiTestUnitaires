import requests
import json
import unittest

from function import *
from classes import *


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.database_manager = DatabaseManager("pyRestApi.db")
        self.database_manager.delete_all_db_elements()
        self.url = "http://127.0.0.1:8000"
        self.headers = {'Content-type': 'application/json'}

    def tearDown(self):
        self.database_manager.delete_all_db_elements()

    '''/ : Main rest api route'''
    def test_main(self):
        response = requests.get(self.url)
        self.assertEqual(response.json()["Code"], "201")


    '''/register : Adding a new user to database if doesn't already exist'''
    def test_register_user(self):
        # Initialize needed informations
        data = {"username": "Flavio", "password": "abcde1234"}
        get_user_request = '''SELECT * FROM users where username = "Flavio"'''

        #Testing user to be added in database
        response = requests.post(
            self.url + "/register", data=json.dumps(data), headers=self.headers)
        self.assertEqual(response.status_code, 200) # Check if server response code is 200
        self.assertEqual(response.json()["Code"], "201") # Check if personalized response code is 201
        self.assertIsNotNone(self.database_manager.make_sql_request(get_user_request)) # check if user well registered into database


        #Testing adding user that already exist
        response = requests.post(
            self.url + "/register", data=json.dumps(data), headers=self.headers)
        self.assertEqual(response.status_code, 200) # Check if server response code is 200
        self.assertEqual(response.json()["Code"], "401") # Check if personalized response code is 401

        #Testing if not giving all needed informations in request body (giving only password in body and not username)
        data = {"password": "newpass"}
        response = requests.post(
            self.url + "/register", data=json.dumps(data), headers=self.headers)
        self.assertEqual(response.status_code, 422)


    '''/modifyUsername : Modifying username for existing user'''
    def test_modify_username(self):
        # Initialize needed informations
        data = {"username": "Flavio", "password": "flavioabcde"}
        get_new_username_request = '''SELECT * FROM users where username = "flav"'''
        get_old_username_request = '''SELECT * FROM users where username = "Flavio"'''
        response = requests.post(
            self.url + "/register", data=json.dumps(data), headers=self.headers)
                

        # Testing modify username "Flavio" by "flav" into database
        response = requests.post(
            self.url + "/modifyUsername?old_user_name=Flavio&new_user_name=flav", headers=self.headers)
        self.assertEqual(response.status_code, 200) # Check if server response code is 200
        self.assertEqual(response.json()["Code"], "201") # Check if personalized response code is 201
        self.assertIsNotNone(self.database_manager.make_sql_request(get_new_username_request)) # check if user username as beig well modified into database
        self.assertIsNone(self.database_manager.make_sql_request(get_old_username_request)) # check if old username is not into database

        # Testing modifying an username not founded
        response = requests.post(
            self.url + "/modifyUsername?old_user_name=Bob&new_user_name=Bo", headers=self.headers)
        self.assertEqual(response.status_code, 200) # Check if server response code is 200
        self.assertEqual(response.json()["Code"], "401") # Check if personalized response code is 401

        #Testing if not giving all needed query params
        response = requests.post(
            self.url + "/modifyUsername?old_user_name=Bo", headers=self.headers)
        self.assertEqual(response.status_code, 422)


    '''/User : Get all users from users SQLITE database'''
    def test_get_all_users(self):
        response = requests.get(self.url + "/User")
        get_users_request = '''SELECT * from users'''

        #Testing if there is none users into database
        self.assertEqual(response.status_code, 200) # Check if server response code is 200
        self.assertEqual(response.json()["Code"], "401") # Check if personalized response code is 401
        self.assertIsNone(self.database_manager.make_sql_request(get_users_request)) # check if none user exist into database

        #Initialize needed informations
        data = {"username": "Flavio", "password": "flavioabcd"}
        data_second = {"username": "Pierre", "password": "Pierreabcd"}
        response = requests.post(
            self.url + "/register", data=json.dumps(data), headers=self.headers)
        response = requests.post(
            self.url + "/register", data=json.dumps(data_second), headers=self.headers)
        
        #Testing getting all users from database when at least one exist
        response = requests.get(self.url + "/User")
        self.assertEqual(response.status_code, 200) # Check if server response code is 200
        self.assertEqual(response.json()["Code"], "201") # Check if personalized response code is 401
        self.assertEqual(response.json()["Server Response"][0], [1, "Flavio", "flavioabcd"])
        self.assertEqual(response.json()["Server Response"][1], [2, "Pierre", "Pierreabcd"])
        self.assertIsNotNone(self.database_manager.make_sql_request(get_users_request)) # check if users exist into database


    '''/insertGames : Insert a game into games SQLITE database'''
    def test_insert_game(self):
        #Initialized neede informations
        data = {"name": "Valorant", "description": "Jeu shooter en première personne développé par Riot Games",
                "genre": "FPS", "annee": 2020, "pegi": 16}
        get_game_request = '''SELECT * from games where name = "Valorant"'''
        response = requests.put(self.url + "/insertGame",
                                data=json.dumps(data), headers=self.headers)
        
        #Testing if game is well added to database
        self.assertEqual(response.status_code, 200) # Check if server response code is 200
        self.assertEqual(response.json()["Code"], "201") # Check if personalized response code is 201
        self.assertIsNotNone(self.database_manager.make_sql_request(get_game_request)) # Check if games exist into database

        #Testing if not giving all needed body params
        data = {"name": "Gta V", "description": "Rockstar Games"}
        response = requests.put(self.url + "/insertGame",
                data=json.dumps(data), headers=self.headers)
        self.assertEqual(response.status_code, 422)


    '''/myGames : Getting all games from games SQLITE database'''
    def test_get_all_games(self):
        get_games_request = '''SELECT * FROM games'''
        response = requests.get(self.url + "/myGames")

        #Testing in case of there is any existing games into database
        self.assertEqual(response.status_code, 200) # Check if server response code is 200
        self.assertEqual(response.json()["Code"], "401") # Check if personalized response code is 401
        self.assertIsNone(self.database_manager.make_sql_request(get_games_request)) # check if none game exist into database


        #Initialized needed informations
        data = {"name": "Valorant", "description": "Jeu shooter en première personne développé par Riot Games",
                "genre": "FPS", "annee": 2020, "pegi": 16}
        response = requests.put(self.url + "/insertGame",
                                data=json.dumps(data), headers=self.headers)
        data = {"name": "GTA V", "description": "JRockstar Games",
                "genre": "Action, TPS, FPS", "annee": 2012, "pegi": 18}
        response = requests.put(self.url + "/insertGame",
                                data=json.dumps(data), headers=self.headers)

        # Testing getting all games stored into database
        response = requests.get(self.url + "/myGames")
        self.assertEqual(response.status_code, 200) # Check if server response code is 200
        self.assertEqual(response.json()["Code"], "201") # Check if personalized response code is 201
        self.assertIsNotNone(self.database_manager.make_sql_request(get_games_request)) # Check if games exist into database

    '''/deleteGame : Delegate a game if it exist from database by name'''
    def test_delete_games(self):
        # Initialize need informations
        get_games_request = '''SELECT * FROM games where name = "Valorant"'''
        data = {"name": "Valorant", "description": "Jeu shooter en première personne développé par Riot Games",
                "genre": "FPS", "annee": 2020, "pegi": 16}
        response = requests.put(self.url + "/insertGame",
                                data=json.dumps(data), headers=self.headers)
        

        #Testing deleting game if exist
        self.assertIsNotNone(self.database_manager.make_sql_request(get_games_request)) # Check if game with name Valorant exist into database

        response = requests.delete(
            self.url + "/deleteGame?game_name=Valorant", headers=self.headers)
        
        self.assertEqual(response.status_code, 200) # Check if server response code is 200
        self.assertEqual(response.json()["Code"], "201") # Check if personalized response code is 201
        self.assertIsNone(self.database_manager.make_sql_request(get_games_request)) # check if game with name that is Valorant do not anymore exist into database


        #Testion deleting game if not exist
        response = requests.delete(
            self.url + "/deleteGame?game_name=Valorant", headers=self.headers)
        
        self.assertEqual(response.status_code, 200) # Check if server response code is 200
        self.assertEqual(response.json()["Code"], "401") # Check if personalized response code is 201
        self.assertIsNone(self.database_manager.make_sql_request(get_games_request)) # check if game with name that is Valorant do not anymore exist into database


class TestDatabaseManager(unittest.TestCase):
    
    def setUp(self):
        self.db_manager = DatabaseManager('pyRestApi.db')

    def test_make_sql_request_users_table(self):

        # Initialized needed informations
        insert_user_request = '''INSERT INTO users(id, username, password) VALUES ("1", "Flavio", "flavioabcd")'''
        select_user_request = '''SELECT * FROM users where username = "Flavio"'''
        update_user_request = '''UPDATE users set username = "Bob" where username = "Flavio"'''

        request_insert_result = self.db_manager.make_sql_request(insert_user_request)
        request_get_result = self.db_manager.make_sql_request(select_user_request)
       
        # Testing return of adding user to SQLITE database
        self.assertEqual(request_insert_result, "Done")

        #Testing return of select query from SQLITE database
        self.assertEqual(request_get_result, [(1, "Flavio", "flavioabcd")])
        self.assertIsNotNone(request_get_result)

        #Testing to update user by username
        request_update_result = self.db_manager.make_sql_request(update_user_request)
        self.assertEqual(request_update_result, "Done")


    def test_make_sql_request_games_table(self):
        # Initialized needed informations
        insert_game_request = '''INSERT INTO games(id, name, description, genre, annee, pegi) VALUES ("1", "Valorant", "Riot games", "FPS", 2020, 16)'''
        select_game_request = '''SELECT * FROM games'''
        delete_game_request = '''DELETE from games'''

        request_insert_result = self.db_manager.make_sql_request(insert_game_request)
        request_get_result = self.db_manager.make_sql_request(select_game_request)

        # Testing return of adding game to SQLITE database
        self.assertEqual(request_insert_result, "Done")

        #Testing return of select query from SQLITE database
        self.assertEqual(request_get_result, [(1, "Valorant", "Riot games", "FPS", 2020, 16)])
        self.assertIsNotNone(request_get_result)

        #Testion to delete games in SQLITE database
        request_delete_result = self.db_manager.make_sql_request(delete_game_request)
        self.assertEqual(request_delete_result, "Done")

    def tearDown(self):
        self.db_manager.delete_all_db_elements()
        self.db_manager.close_sql_connection()

if __name__ == "__main__":
    unittest.main()