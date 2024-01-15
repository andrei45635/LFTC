from typing import List

from symbols.nonterminal import Nonterminal
from symbols.symbol import Symbol


class Production:
    def __init__(self, lhs: Nonterminal, rhs: List[Symbol]):
        self.__lhs = lhs
        self.__rhs = rhs

    @property
    def lhs(self):
        return self.__lhs

    @property
    def rhs(self):
        return self.__rhs

    def __eq__(self, other) -> bool:
        return isinstance(other, Production) and self.__dict__ == other.__dict__

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __repr__(self):
        return f'{repr(self.__lhs)}->{" ".join([repr(symbol) for symbol in self.__rhs])}'

    def __str__(self):
        return repr(self)
