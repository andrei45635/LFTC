from symbols.symbol import Symbol


class Dollar(Symbol):
    def __init__(self):
        super(Dollar, self).__init__("$")
        self.__dollar = "$"

    @staticmethod
    def check_symbol(s: str) -> bool:
        return s == "$"
