from .team_member import TeamMember
from .identified_object import IdentifiedObject
from .exceptions import DuplicateEmail, DuplicateOid


class Team(IdentifiedObject):
    def __init__(self, oid, name):
        super().__init__(oid)
        self._name = name
        self._members = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,name):
        self._name = name

    @property
    def members(self):
        return self._members

    def add_member(self, member):
        if any(m for m in self.members if m.oid == member.oid):
            raise DuplicateOid(member.oid)

        if any(m for m in self.members if m.email.lower() == member.email.lower()):
            raise DuplicateEmail(member.email)

        self.members.append(member)

    def member_named(self, s):
        for member in self._members:
            if member.name == s:
                return member
        return None

    def remove_member(self, member):
        if member in self._members:
            self._members.remove(member)

    def send_email(self, emailer, subject, message):
        recipient_emails = [member.email for member in self.members if member.email]
        emailer.send_plain_email(recipient_emails, subject, message)

    def __str__(self):
        return f"Team Name: {self.name}, {len(self.members)} members"
