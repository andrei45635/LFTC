from symbols.nonterminal import Nonterminal


class Grammar:
    def __init__(self, terminals, nonterminals, productions):
        self.__terminals = terminals
        self.__nonterminals = nonterminals
        self.__productions = productions
        self.__start_symbol = productions[0].lhs

    @property
    def get_terminals(self):
        return self.__terminals

    @property
    def get_nonterminals(self):
        return self.__nonterminals

    @property
    def get_productions(self):
        return self.__productions

    @property
    def get_start_symbol(self):
        return self.__start_symbol

    def __repr__(self):
        newline = '\n'
        return f"Nonterminals: {', '.join(repr(nonterminal) for nonterminal in self.__nonterminals)}\n" + \
            f"Terminals: {', '.join(repr(terminal) for terminal in self.__terminals)}\n" + \
            f"Production rules:\n{newline.join(repr(production_rule) for production_rule in self.__productions)}\n "

    def __str__(self):
        return repr(self)

    def get_productions_by_nonterminal_lhs(self, nonterminal: Nonterminal):
        matching_prods = []
        if nonterminal not in self.__nonterminals:
            return []

        for prod in self.__productions:
            if prod.lhs == nonterminal:
                matching_prods.append(prod)

        return matching_prods

    def get_productions_by_nonterminal_rhs(self, nonterminal: Nonterminal):
        matching_prods = []
        if nonterminal not in self.__nonterminals:
            return []

        for prod in self.__productions:
            if prod.rhs == nonterminal:
                matching_prods.append(prod)

        return matching_prods
