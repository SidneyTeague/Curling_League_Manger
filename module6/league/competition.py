from .identified_object import IdentifiedObject
from .team import Team

from datetime import datetime


class Competition(IdentifiedObject):
    def __init__(self, oid, teams, location, date_time=None):
        super().__init__(oid)
        self._teams = teams
        self._location = location
        self._date_time = date_time

    @property
    def teams_competing(self):
        return self._teams

    @property
    def date_time(self):
        return self._date_time

    @date_time.setter
    def date_time(self, date_time):
        self._date_time = date_time

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = location

    def send_email(self, emailer, subject, message):
        recipients = set(member.email for team in self._teams for member in team.members if member.email is not None)
        for recipient in recipients:
            emailer.send_plain_email(recipient, subject, message)

    def __str__(self):
        date_str = self.date_time.strftime("%m/%d/%Y %H:%M") if self.date_time else ""
        return f"Competition at {self.location} on {date_str} with {len(self.teams_competing)} teams"

