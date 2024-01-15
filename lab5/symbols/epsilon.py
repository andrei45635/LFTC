from symbols.symbol import Symbol


class Epsilon(Symbol):
    def __init__(self):
        super(Epsilon, self).__init__("epsilon")
        self.__dollar = "epsilon"

    @staticmethod
    def check_symbol(s: str) -> bool:
        return s == "epsilon"
