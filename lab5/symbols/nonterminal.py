import re

from symbols.symbol import Symbol


class Nonterminal(Symbol):
    def __init__(self, symbol):
        super(Nonterminal, self).__init__(symbol)
        self.__nonterminal = "NONTERMINAL"

    @staticmethod
    def check_symbol(s: str) -> bool:
        return re.match("[A-Z_']+", s) is not None and s.isupper()

    def __repr__(self):
        return f'T:{self._symbol}'
