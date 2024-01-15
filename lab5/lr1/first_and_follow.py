from typing import Dict, Set

from grammar.grammar import Grammar
from symbols.dollar import Dollar
from symbols.epsilon import Epsilon
from symbols.nonterminal import Nonterminal
from symbols.symbol import Symbol
from symbols.terminal import Terminal


class First:
    def __init__(self, grammar: Grammar):
        self.__grammar = grammar
        self.__first: Dict[Nonterminal, Set[Symbol]] = {}
        self.find_first()

    def find_first(self):
        epsilon = Epsilon()

        # Initialize First sets for each nonterminal
        for nonterm in self.__grammar.get_nonterminals:
            self.__first[nonterm] = set()

        modified = True
        while modified:
            modified = False
            for nonterm in self.__grammar.get_nonterminals:
                for prod in self.__grammar.get_productions_by_nonterminal_lhs(nonterm):
                    can_produce_epsilon = True
                    for symbol in prod.rhs:
                        if can_produce_epsilon:
                            if isinstance(symbol, Terminal):
                                # Add terminal and break
                                if symbol not in self.__first[nonterm]:
                                    self.__first[nonterm].add(symbol)
                                    modified = True
                                can_produce_epsilon = False
                            elif isinstance(symbol, Nonterminal):
                                # Add First set of nonterminal, excluding epsilon
                                original_size = len(self.__first[nonterm])
                                self.__first[nonterm].update(self.__first[symbol] - {epsilon})

                                # Check if epsilon is in the First set of the nonterminal
                                can_produce_epsilon = epsilon in self.__first[symbol]

                                if len(self.__first[nonterm]) > original_size:
                                    modified = True

                        if not can_produce_epsilon:
                            break

                    if can_produce_epsilon:
                        self.__first[nonterm].add(epsilon)

            if not modified:
                break

    def get_first_of_nonterminal(self, nonterminal: Nonterminal):
        if nonterminal in self.__first:
            return self.__first[nonterminal]
        return set()

    @property
    def first(self) -> Dict[Nonterminal, Set[Symbol]]:
        return self.__first

    def __repr__(self):
        newline = '\n'
        return f"=== First ===\n{newline.join([repr(entry) for entry in self.__first.items()])}\n"

    def __str__(self):
        return repr(self)

    def get_first_of_sequence(self, sequence):
        first_set = set()
        for symbol in sequence:
            if isinstance(symbol, Terminal):
                first_set.add(symbol)
                break
            elif isinstance(symbol, Nonterminal):
                first_set.update(self.get_first_of_nonterminal(symbol) - {Epsilon()})
                if Epsilon() not in self.get_first_of_nonterminal(symbol):
                    break
        return first_set


class Follow:
    def __init__(self, grammar: Grammar):
        self.__grammar = grammar
        self.__follow: Dict[Nonterminal, Set[Symbol]] = {}
        self.__compute_follow()

    def __compute_follow(self):
        for nonterm in self.__grammar.get_nonterminals:
            self.__follow[nonterm] = set()
        self.__follow[self.__grammar.get_start_symbol] = {Dollar()}

        modified = True
        while modified:
            modified = False
            for prod in self.__grammar.get_productions:
                follow_set_changed = self.__update_follow_set(prod)
                if follow_set_changed:
                    modified = True

    def __update_follow_set(self, prod):
        first = First(self.__grammar)
        changed = False
        A = prod.lhs
        for i in range(len(prod.rhs)):
            B = prod.rhs[i]
            if isinstance(B, Nonterminal):
                # Beta is the sequence after the nonterminal B in the RHS
                beta = prod.rhs[i + 1:]
                follow_B = self.__follow[B]
                first_beta = first.get_first_of_sequence(beta) - {Epsilon()}
                if not follow_B.issuperset(first_beta):
                    follow_B.update(first_beta)
                    changed = True

                # If Beta can produce epsilon or is empty, add Follow(A) to Follow(B)
                if not beta or Epsilon() in first.get_first_of_sequence(beta):
                    if not follow_B.issuperset(self.__follow[A]):
                        follow_B.update(self.__follow[A])
                        changed = True

        return changed

    def get_follow_of_nonterminal(self, nonterminal: Nonterminal):
        if nonterminal in self.__follow:
            return self.__follow[nonterminal]
        return set()

    @property
    def follow(self) -> Dict[Nonterminal, Set[Symbol]]:
        return self.__follow

    def __repr__(self):
        newline = '\n'
        return f"=== Follow ===\n{newline.join([repr(entry) for entry in self.__follow.items()])}\n"

    def __str__(self):
        return repr(self)
