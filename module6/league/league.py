from .competition import Competition
from .identified_object import IdentifiedObject
from .exceptions import DuplicateOid


class League(IdentifiedObject):
    def __init__(self, oid, name):
        super().__init__(oid)
        self._name = name
        self._teams = []
        self._competitions = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def teams(self):
        return self._teams

    @property
    def competitions(self):
        return self._competitions

    def add_team(self, team):
        if any(t for t in self.teams if t.oid == team.oid):
            raise DuplicateOid(team.oid)

        self.teams.append(team)

    def remove_team(self, team):
        # Check if team is in any competitions
        if any(team in competition.teams_competing for competition in self._competitions):
            raise ValueError("The team is involved in a competition and can't be removed.")
        if team in self._teams:
            self._teams.remove(team)

    def team_named(self, team_name):
        for team in self._teams:
            if team.name == team_name:
                return team
        return None

    def add_competition(self, competition):
        # Check if all teams in competition are part of this league
        if not all(team in self.teams for team in competition.teams_competing):
            raise ValueError("One or more teams in the competition are not part of this league.")
        self._competitions.append(competition)

    def teams_for_member(self, member):
        return [team for team in self._teams if member in team.members]

    def competitions_for_team(self, team):
        return [comp for comp in self._competitions if team in comp.teams_competing]

    def competitions_for_member(self, member):
        teams = self.teams_for_member(member)
        return [comp for comp in self._competitions if any(team in comp.teams_competing for team in teams)]

    def __str__(self):
        return f"League Name: {self.name}, {len(self.teams)} teams, {len(self.competitions)} competitions"

