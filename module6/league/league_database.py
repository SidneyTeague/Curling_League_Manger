import pickle
import os
import csv
from .team import Team
from .team_member import TeamMember


class LeagueDatabase:
    _sole_instance = None
    _last_oid = 0

    def __init__(self):
        self.leagues = []

    @classmethod
    def instance(cls):
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    @classmethod
    def load(cls, file_name):
        try:
            with open(file_name, 'rb') as file:
                cls._sole_instance = pickle.load(file)
        except (FileNotFoundError, pickle.PickleError) as e:
            if "backup" not in file_name:
                print(f"Error loading database from file: {e}. Loading from backup...")
                cls.load(file_name + '.backup')
            else:
                print('Backup file not found. Please ensure the required file exists.')

    def add_league(self, league):
        self.leagues.append(league)

    def remove_league(self, league):
        if league in self.leagues:
            self.leagues.remove(league)

    def league_named(self, name):
        for league in self.leagues:
            if league.name == name:
                return league
        return None

    @classmethod
    def next_oid(cls):
        cls._last_oid += 1
        return cls._last_oid

    def save(self, file_name):
        backup_file_name = file_name + '.backup'
        if os.path.exists(backup_file_name):
            os.remove(backup_file_name)
        if os.path.exists(file_name):
            os.rename(file_name, backup_file_name)
        with open(file_name, 'wb') as file:
            pickle.dump(self, file)

    def import_league_teams(self, league, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for team_name, team_member, email in reader:
                    team = league.team_named(team_name)
                    if not team:
                        team = Team(self.next_oid(), team_name)
                        league.add_team(team)
                        print(f"Team '{team_name}' added to league '{league.name}'")
                    member = TeamMember(self.next_oid(), team_member, email)
                    team.add_member(member)
        except (FileNotFoundError, csv.Error) as e:
            print(f"Error importing teams: {e}")

    @staticmethod
    def export_league_teams(league, file_name):
        try:
            with open(file_name, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Team name", "Member name", "Member email"])
                for team in league.teams:
                    for member in team.members:
                        writer.writerow([team.name, member.name, member.email])
        except (FileNotFoundError, csv.Error) as e:
            print(f"Error exporting teams: {e}")
