from abc import ABC


class IdentifiedObject(ABC):
    def __init__(self, oid):
        self._oid = oid

    @property
    def oid(self):
        return self._oid

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._oid == other.oid

    def __hash__(self):
        return hash(self._oid)
