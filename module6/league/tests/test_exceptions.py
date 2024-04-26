import unittest
from league.exceptions import DuplicateOid, DuplicateEmail
from league.league import League
from league.team import Team
from league.competition import Competition
from league.team_member import TeamMember


class TestSuite(unittest.TestCase):
    def setUp(self):
        self.league = League(1, "League1")
        self.team1 = Team(1, "Team1")
        self.team2 = Team(2, "Team2")
        self.league.add_team(self.team1)
        self.member1 = TeamMember(1, "Member1", "member1@gmail.com")
        self.member2 = TeamMember(2, "Member2", "member2@gmail.com")

    def test_duplicate_oid(self):
        self.team1.add_member(TeamMember(1, "DuplicateOID", "duplicate@gmail.com"))
        with self.assertRaises(DuplicateOid):
            self.team1.add_member(TeamMember(1, "DuplicateOID2", "duplicate2@gmail.com"))

    def test_duplicate_email_case_insensitive(self):
        self.team1.add_member(TeamMember(3, "Member3", "MEMBER3@gmail.com"))
        with self.assertRaises(DuplicateEmail):
            self.team1.add_member(TeamMember(4, "Member4", "member3@gmail.com"))

    def test_team_in_league_competition(self):
        competition = Competition(1, [self.team1, self.team2], "Competition1")
        with self.assertRaises(ValueError):
            self.league.add_competition(competition)

    def test_remove_team_in_competition(self):
        competition = Competition(1, [self.team1], "Competition1")
        self.league.add_team(self.team2)
        self.league.add_competition(competition)
        with self.assertRaises(ValueError):
            self.league.remove_team(self.team1)
