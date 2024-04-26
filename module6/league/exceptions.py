class DuplicateEmail(Exception):
    """
    Exception raised when a duplicate email is encountered.

    Attributes:
        email -- the duplicate email that caused the exception
    """

    def __init__(self, email):
        self.email = email
        super().__init__(f'Duplicate Email encountered: {self.email}')


class DuplicateOid(Exception):
    """
    Exception raised when a duplicate OID is encountered.

    Attributes:
        oid -- the duplicate OID that caused the exception
    """

    def __init__(self, oid):
        self.oid = oid
        super().__init__(f'Duplicate OID encountered: {self.oid}')
