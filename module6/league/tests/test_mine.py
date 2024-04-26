# My own unit test
import unittest
from datetime import datetime
from league.league import League
from league.team import Team
from league.team_member import TeamMember
from league.competition import Competition


class TestLeague(unittest.TestCase):  # Expected test results: Tests failed: 3, passed: 5 to 8 test
    def test_str(self):
        league = League(1, "AL State Curling League")
        self.assertEqual(str(league), "League Name: AL State Curling League, 0 teams, 0 competitions")

    def test_str_team(self):
        team = Team(1, "Team 1")
        self.assertEqual(str(team), "Team Name: Team 1, 0 members")

    def test_str_competition(self):
        teams = [Team(1, "Team 1"), Team(2, "Team 2")]
        competition = Competition(1, teams, "Location 1", datetime(2024, 4, 1))
        self.assertEqual(str(competition), "Competition at Location 1 on 04/01/2024 00:00 with 2 teams")

    # I want this test to fail
    def test_remove_team_not_in_league(self):
        league = League(1, "Test League")
        team = Team(1, "Team 1")
        with self.assertRaises(ValueError,
                               msg="Attempting to remove a team not present in the league should raise a ValueError"):
            league.remove_team(team)

    def test_team_named_existing_team(self):
        league = League(1, "Test League")
        team1 = Team(1, "Team 1")
        team2 = Team(2, "Team 2")
        league.add_team(team1)
        league.add_team(team2)
        self.assertEqual(league.team_named("Team 1"), team1)

    def test_team_named_non_existing_team(self):
        league = League(1, "Test League")
        team1 = Team(1, "Team 1")
        team2 = Team(2, "Team 2")
        league.add_team(team1)
        league.add_team(team2)
        self.assertIsNone(league.team_named("Team 3"))

    # I want this test to fail too
    def test_add_duplicate_member(self):
        team = Team(1, "Team 1")
        member = TeamMember(1, "John Doe", "john@example.com")
        team.add_member(member)
        self.assertIn(member, team.members)
        with self.assertRaises(ValueError,  msg="Attempting to add a duplicate member should not be added to the team "
                                                "should raise a ValueError"):
            team.add_member(member)
        self.assertEqual(len(team.members), 1)

    # I want this test to fail too
    def test_remove_member_not_in_team(self):
        team = Team(1, "Team 1")
        member = TeamMember(1, "John Doe", "john@example.com")
        with self.assertRaises(ValueError, msg="Attempting to remove a member has not been added to the team "
                               "should raise a ValueError"):
            team.remove_member(member)
