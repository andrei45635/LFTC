from symbols.epsilon import Epsilon
from symbols.nonterminal import Nonterminal


class LR0Item:
    def __init__(self, production):
        self.__production = production
        self.__dot_index = 0

    @property
    def production(self):
        return self.__production

    @property
    def dot_index(self):
        return self.__dot_index

    @property
    def current_symbol(self):
        return self.__production.rhs[self.__dot_index]

    @property
    def is_final_item(self):
        return self.__dot_index == len(self.__production.rhs)

    def solve(self, symbol):
        if not self.__production.rhs[self.__dot_index] == symbol:
            raise RuntimeError(f'Cannot solve {symbol} in LR0Item')
        item = LR0Item(self.__production)
        item.__dot_index = self.__dot_index + 1
        return item

    def __eq__(self, other):
        return isinstance(other, LR0Item) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__production)

    def __repr__(self):
        return f'{repr(self.__production)} with dot at {self.__dot_index}'

    def __str__(self):
        return repr(self)


class Closure:
    def __init__(self, grammar, lr0items):
        self.__grammar = grammar
        self.__lr0items = lr0items
        self.__apply_closure()

    @property
    def lr0items(self):
        return self.__lr0items

    @property
    def is_final_closure(self):
        for lr0item in self.__lr0items:
            if not (lr0item.is_final_item or lr0item.current_symbol == Epsilon()):
                return False
        return True

    @property
    def no_final_items(self) -> int:
        i = 0
        for lr0item in self.__lr0items:
            if lr0item.is_final_item:
                i += 1
        return i

    def __eq__(self, other) -> bool:
        return isinstance(other, Closure) and self.__dict__ == other.__dict__

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return sum([hash(item) for item in self.__lr0items])

    def __repr__(self):
        return '\n'.join([repr(item) for item in self.__lr0items])

    def __str__(self):
        return repr(self)

    def __apply_closure(self):
        def __apply_closure__(lr0item):
            if lr0item in lr0items or lr0item.is_final_item or not isinstance(lr0item.current_symbol, Nonterminal):
                return
            for prod in self.__grammar.get_productions_by_nonterminal_lhs(lr0item.current_symbol):
                new_lr0item = LR0Item(prod)
                if new_lr0item != lr0item:
                    __apply_closure__(new_lr0item)
                    if new_lr0item not in lr0items:
                        lr0items.append(new_lr0item)
        lr0items = []
        for item in self.__lr0items:
            __apply_closure__(item)
        self.__lr0items.extend(lr0items)


class ClosureTransition:
    def __init__(self, symbol, from_index, to_index):
        self.__symbol = symbol
        self.__from_index = from_index
        self.__to_index = to_index

    @property
    def symbol(self):
        return self.__symbol

    @property
    def from_index(self):
        return self.__from_index

    @property
    def to_index(self):
        return self.__to_index

    def __repr__(self):
        return f"from {self.__from_index} with {self.__symbol} to {self.__to_index}"

    def __str__(self):
        return repr(self)
