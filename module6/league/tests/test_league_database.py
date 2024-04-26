import unittest
import os
from league.league_database import LeagueDatabase
from league.league import League
from league.team import Team
from league.team_member import TeamMember


class TestLeagueDatabase(unittest.TestCase):
    def setUp(self):
        self.database = LeagueDatabase.instance()
        self.database.load('database.pkl')
        self.league = League(LeagueDatabase.next_oid(), "Test League")
        self.database.add_league(self.league)
        # Add some teams and members to the league for testing
        team1 = Team(LeagueDatabase.next_oid(), "Team 1")
        team1.add_member(TeamMember(LeagueDatabase.next_oid(), "Alice", "alice@example.com"))
        team1.add_member(TeamMember(LeagueDatabase.next_oid(), "Bob", "bob@example.com"))
        self.league.add_team(team1)

    def tearDown(self):
        self.database.save('database.pkl')

    def test_import_league_teams(self):
        file_name = 'Teams.csv'
        self.database.import_league_teams(self.league, file_name)
        team_names = [team.name for team in self.league.teams]
        expected_team_names = ["Flintstones", "Curl Jam", "Curl Power", "Cold Fingers", "Team 1"]
        self.assertEqual(sorted(team_names), sorted(expected_team_names))

    def test_export_league_teams(self):
        file_name = 'exported_teams.csv'
        self.database.export_league_teams(self.league, file_name)
        # Check if the file was created
        self.assertTrue(os.path.exists(file_name))
        # Check the content of the file
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            self.assertEqual(lines[0].strip(), "Team name,Member name,Member email")
            self.assertEqual(lines[1].strip(), "Team 1,Alice,alice@example.com")
            self.assertEqual(lines[2].strip(), "Team 1,Bob,bob@example.com")

        # Clean up the exported file
        os.remove(file_name)

