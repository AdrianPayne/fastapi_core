from unittest import TestCase

from ..models import Hero, Team
from ...db.connection import DbSession


class TestExampleModels(TestCase):
    """
    This test suit has the intention to validate a way to declare models using SQLModel
    and specifically, the Relationship attribute.
    """

    def setUp(self) -> None:
        DbSession.create_tables()

    def tearDown(self):
        Hero.delete_table(Hero)
        Team.delete_table(Team)

    def test_read_relationship(self):
        """ Check if we can read the relational object """
        heroes = [
            {'name': "Batman", 'team_id': 1, "secret_password": "my_password"},
            {'name': "Superman", 'team_id': 1, "secret_password": "my_password"},
            {'name': "Hitler", 'team_id': 1, "secret_password": "my_password"},
            {'name': "Spiderman", 'team_id': 2, "secret_password": "my_password"},
            {'name': "Stalin", 'team_id': 2, "secret_password": "my_password"},
            {'name': "Pato Lucas", 'team_id': 2, "secret_password": "my_password"},
        ]
        teams = [
            {'name': 'axis'},
            {'name': 'people'}
        ]

        for team in teams:
            Team(**team).create()

        for hero in heroes:
            Hero(**hero).create()

        heroes_db = Hero.get_all(Hero)
        team_db = Team.get_all(Team)

        self.assertEqual(heroes[0]['name'], heroes_db[0].name)
        self.assertEqual(team_db[0].name, heroes_db[0].team.name)

    def test_modify_though_relationship(self):
        """ Check if can modify models from the relational models"""
        hero = {'name': "Batman", 'team_id': 1, "secret_password": "my_password"}
        team = {'name': 'axis'}
        new_team_name = 'Avengers'

        Team(**team).create()
        hero_db = Hero(**hero).create()
        hero_db.team.update({'name': new_team_name})
        team_db = Team.get_one(Team, 1)

        self.assertEqual(new_team_name, team_db.name)
