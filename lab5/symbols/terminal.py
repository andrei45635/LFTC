import re

from symbols.symbol import Symbol


class Terminal(Symbol):
    def __init__(self, symbol):
        super(Terminal, self).__init__(symbol)
        self.__terminal = "TERMINAL"

    @staticmethod
    def check_symbol(s: str) -> bool:
        return s.islower()
        # return re.match('[^A-Z]+', s) is not None and s.islower()

    def __repr__(self):
        return f"t:{self._symbol}"
