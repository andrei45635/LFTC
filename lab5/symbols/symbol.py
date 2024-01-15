class Symbol:
    def __init__(self, symbol):
        self._symbol = symbol

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, value: str):
        self._symbol = value

    @staticmethod
    def check_symbol(s: str) -> bool:
        return bool(s)

    def __repr__(self):
        return f"S:{self._symbol}"

    def __str__(self):
        return repr(self)

    def __eq__(self, other) -> bool:
        return isinstance(other, Symbol) and self.__dict__ == other.__dict__

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self._symbol)
