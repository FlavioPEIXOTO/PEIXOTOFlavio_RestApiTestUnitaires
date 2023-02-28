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

    def test_root_endpoint(self):
        response = requests.get(self.url)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.content, '{"Code": "201", "ServerResponse" : "Welcome to GamingLibrary, an api rest to store games locally \n Also you can add users to manage too your game list"}')

    def test_register_user(self):
        data = {"username": "Flavio", "password": "abcde1234"}
        response = requests.post(
            self.url + "/register", data=json.dumps(data), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["Code"], "201")

        response = requests.post(
            self.url + "/register", data=json.dumps(data), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["Code"], "401")

    def test_modify_username(self):
        data = {"username": "Flavio", "password": "flavioabcde"}
        response = requests.post(
            self.url + "/register", data=json.dumps(data), headers=self.headers)
        self.assertEqual(response.status_code, 200)

        # data = {"old_user_name": "Flavio", "new_user_name": "flav"}
        response = requests.post(
            self.url + "/modifyUsername?old_user_name=Flavio&new_user_name=flav", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["Code"], "201")

        # Modifying an username not founded
        # response = requests.post(
        #    self.url + "/modifyUsername", data=json.dumps(data), headers=self.headers)
        response = requests.post(
            self.url + "/modifyUsername?old_user_name=Bob&new_user_name=Bo", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["Code"], "401")

    def test_get_all_users(self):
        data = {"username": "Bob", "password": "Bobabcd"}
        data_second = {"username": "Pierre", "password": "Pierreabcd"}
        response = requests.post(
            self.url + "/register", data=json.dumps(data), headers=self.headers)
        response = requests.post(
            self.url + "/register", data=json.dumps(data_second), headers=self.headers)

        response = requests.get(self.url + "/User")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["Code"], "201")

    def test_insert_game(self):
        data = {"name": "Valorant", "description": "Jeu shooter en première personne développé par Riot Games",
                "genre": "FPS", "annee": 2020, "pegi": 16}
        response = requests.put(self.url + "/insertGame",
                                data=json.dumps(data), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["Code"], "201")

    def test_get_all_games(self):
        data = {"name": "Valorant", "description": "Jeu shooter en première personne développé par Riot Games",
                "genre": "FPS", "annee": 2020, "pegi": 16}
        response = requests.put(self.url + "/insertGame",
                                data=json.dumps(data), headers=self.headers)

        data_second = {"name": "League of Legends", "description": "Jeu tps développé par Riot Games",
                       "genre": "FPS", "annee": 2020, "pegi": 16}
        response = requests.put(self.url + "/insertGame",
                                data=json.dumps(data_second), headers=self.headers)

        response = requests.get(self.url + "/myGames")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["Code"], "201")


if __name__ == "__main__":
    unittest.main()
