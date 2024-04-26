from .identified_object import IdentifiedObject


class TeamMember(IdentifiedObject):
    def __init__(self, oid, name, email):
        super().__init__(oid)
        self._name = name
        self._email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    def send_email(self, emailer, subject, message):
        if self._email is not None:
            emailer.send_plain_email([self._email], subject, message)

    def __str__(self):
        return f"{self.name}<{self.email}>"
