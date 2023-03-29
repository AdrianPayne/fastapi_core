from unittest import TestCase
from fastapi.testclient import TestClient

from ..views import app
from ..models import Hero, Team
from ...db.connection import DbSession


class TestExampleViews(TestCase):

    client = TestClient(app)

    hero_data_create_1 = {"name": "Spiderman", "team_id": 1, "secret_password": "my_password1"}
    hero_data_create_2 = {"name": "Iron Man", "team_id": 1, "secret_password": "my_password2"}
    hero_data_create_3 = {"name": "Superman", "team_id": 2, "secret_password": "my_password3"}
    team_data_create_1 = {"name": "Avengers"}
    team_data_create_2 = {"name": "Justice League"}

    def setUp(self) -> None:
        DbSession.create_tables()
        # Heroes
        hero_1 = Hero(**self.hero_data_create_1).create()
        hero_2 = Hero(**self.hero_data_create_2).create()
        hero_3 = Hero(**self.hero_data_create_3).create()
        self.hero_list = [hero_1, hero_2, hero_3]
        # Teams
        team_1 = Team(**self.team_data_create_1).create()
        team_2 = Team(**self.team_data_create_2).create()
        self.team_list = [team_1, team_2]

    def tearDown(self):
        Hero.delete_table(Hero)
        Team.delete_table(Team)

    def test_create_hero(self):
        # Given
        hero_data_create = {"name": "Spiderman", "team_id": 1, "password": "my_password"}

        # When Create
        response = self.client.post('/hero', json=hero_data_create)
        hero_id = response.json()["id"]

        # Then Create
        assert response.status_code == 201
        assert response.json()["name"] == hero_data_create["name"]
        assert response.json()["team_id"] == hero_data_create["team_id"]

    def test_update_hero(self):
        # Given
        hero_data_update = {'name': 'Batman'}
        hero_id = 1

        # When Update
        response = self.client.put(f'/hero/{hero_id}', json=hero_data_update)

        # Then Update
        assert response.status_code == 200
        assert response.json()["name"] == hero_data_update["name"]

    def test_delete_hero(self):
        # Given
        hero_id = 1

        # When
        response = self.client.delete(f'/hero/{hero_id}')

        # Then
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.json()[0])
        self.assertEqual('success', response.json()[1])

    def test_get_one_hero(self):
        # Given
        hero_id = 1

        # When
        response = self.client.get(f'/hero/{hero_id}')

        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual(hero_id, response.json()['id'])
        self.assertEqual(self.team_data_create_1['name'], response.json()['team']['name'])

    def test_get_all_hero(self):
        response = self.client.get("/hero?offset=0&limit=100")

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIsInstance(response_data, list)
        self.assertEqual(len(self.hero_list), len(response_data))

        for i, hero in enumerate(self.hero_list):
            self.assertEqual(hero.id, response_data[i]["id"])
            self.assertEqual(hero.name, response_data[i]["name"])
            self.assertEqual(hero.team_id, response_data[i]["team_id"])

    def test_create_hero_ko_duplicate(self):
        # Llamar a la API para crear un héroe con el mismo nombre
        new_hero = {"name": "Iron Man", "team_id": 1, "secret_password": "my_password2"}
        response = self.client.post("/hero", json=new_hero)

        # Comprobar que se recibe una respuesta con código HTTP 422
        self.assertEqual(response.status_code, 422)

    def test_update_hero_ko_not_found(self):
        # Llamar a la API para actualizar un héroe que no existe
        response = self.client.put("/hero/99", json=self.hero_data_create_1)

        # Comprobar que se recibe una respuesta con código HTTP 404
        self.assertEqual(response.status_code, 404)

        # Comprobar que se recibe un mensaje de error adecuado
        expected_error = {"detail": "This hero was not found"}
        self.assertEqual(response.json(), expected_error)

    def test_delete_hero_ko_not_found(self):
        # Llamar a la API para eliminar un héroe que no existe
        response = self.client.delete("/hero/10000")

        # Comprobar que se recibe una respuesta con código HTTP 404
        self.assertEqual(response.status_code, 404)

        # Comprobar que se recibe un mensaje de error adecuado
        expected_error = {"detail": "This hero was not found"}
        self.assertEqual(response.json(), expected_error)