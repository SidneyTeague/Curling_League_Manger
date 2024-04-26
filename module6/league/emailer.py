import yagmail
import os


class Emailer:
    sender_address = None
    _sole_instance = None
    _yag = None

    def __new__(cls):
        if cls._sole_instance is None:
            cls._sole_instance = super().__new__(cls)
        return cls._sole_instance

    @classmethod
    def configure(cls):
        cls.sender_address = os.getenv('teaguesr0040')
        cls._yag = yagmail.SMTP(cls.sender_address)

    @classmethod
    def instance(cls):
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    def send_plain_email(self, recipients, subject, message):
        # Check if 'recipients' is a string, convert to a list if necessary
        if isinstance(recipients, str):
            recipients = [recipients]

        # Iterating over each recipient and sending email
        for recipient in recipients:
            print(f"Sending mail to: {recipient}")
            try:
                self._yag.send(to=recipient, subject=subject, contents=message)
                print(f"Mail sent successfully to {recipient}")
            except Exception as e:
                print(f"Error occurred while sending mail to {recipient} : {e}")

        return recipients

    def __init__(self):
        if Emailer._sole_instance:
            raise Exception("This class is a singleton!")
        else:
            Emailer._sole_instance = self
