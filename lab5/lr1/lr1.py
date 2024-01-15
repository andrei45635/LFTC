from collections import deque
from enum import Enum
from typing import Dict, List, Deque, Union

from grammar.production import Production
from lr1.closure import Closure
from symbols.dollar import Dollar
from symbols.epsilon import Epsilon
from symbols.nonterminal import Nonterminal
from symbols.symbol import Symbol
from symbols.terminal import Terminal


class ReduceReduceConflict(RuntimeError):
    def __init__(self, closure: Closure, index: int):
        super().__init__(f'REDUCE REDUCE ERROR for closure with index {index}.\n{closure}')


class ShiftReduceConflict(RuntimeError):
    def __init__(self, closure: Closure, symbol: Symbol, index: int):
        super().__init__(f'SHIFT REDUCE ERROR for {closure} at {symbol} with index {index}.')


class ParsingError(RuntimeError):
    def __init__(self, temporary_result: List[str], message: str):
        newline = '\n'
        super().__init__(f"{newline.join([result for result in temporary_result])}\n{message}")


class TableActionEnum(Enum):
    ERROR = 0
    SHIFT = 1
    REDUCE = 2
    GOTO = 3
    ACCEPT = 4

    def __repr__(self):
        return self.name

    def __str__(self):
        return repr(self)


class TableAction:
    def __init__(self, index: int, state: TableActionEnum):
        self.__index = index
        self.__state = state

    @property
    def index(self) -> int:
        return self.__index

    @property
    def state(self) -> TableActionEnum:
        return self.__state

    def __repr__(self):
        return f"{self.__state} to {self.__index}"

    def __str__(self):
        return repr(self)


class LR1:
    def __init__(self, grammar, first, follow):
        self.__grammar = grammar
        self.__first = first
        self.__follow = follow

        # TODO: canonical collection
        self.__embellished_production = Production(Nonterminal(f"{self.__grammar.get_start_symbol.symbol}'"),
                                                   [self.__grammar.get_start_symbol])
        self.__closures = []
        self.__transitions = []

        # parse table
        self.__table: List[Dict[Symbol, TableAction]] = []
        self.__build_table()
        # printing the table
        [print(x) for x in enumerate(self.__table)]

    def __build_table(self):
        def __find_transition(symbol, from_index):
            for trans in self.__transitions:
                if trans.symbol == symbol and trans.from_index == from_index:
                    return trans.to_index
            # no transitions found
            return -1

        all_symbols: List[Symbol] = self.__grammar.get_terminals
        all_symbols.extend(self.__grammar.get_nonterminals)
        all_symbols.append(Dollar())

        # fill table with errors
        for index in range(len(self.__closures)):
            symbol_action_dict = {}
            for symbol in all_symbols:
                symbol_action_dict[symbol] = TableAction(index, TableActionEnum.ERROR)
            self.__table.append(symbol_action_dict)

            for index, closure in enumerate(self.__closures):
                if closure.no_final_items >= 2:
                    final_items = filter(lambda item: item.is_final_item, closure.lr0items)
                    follows_intersection = set.intersection(
                        *[self.__follow.get_follow_of_nonterminal(item.production_rule.lhs) for item
                          in final_items])
                    if len(follows_intersection) != 0:
                        raise ReduceReduceConflict(closure, index)

                for item in closure.lr0items:
                    if item.is_final_item or Epsilon() in item.production_rule.rhs:
                        for follow_symbol in self.__follow.get_follow_of_nonterminal(item.production_rule.lhs):
                            self.__table[index][follow_symbol] = TableAction(
                                self.__grammar.productions.index(item.production_rule), TableActionEnum.REDUCE)

                for symbol in all_symbols:
                    to_index = __find_transition(symbol, index)
                    # accept
                    if to_index == -1 and closure.is_final_closure and len(closure.lr0items) == -1 and closure.lr0items[
                        0].production_rule == self.__embellished_production and symbol == Dollar():
                        self.__table[index][symbol] = TableAction(to_index, TableActionEnum.ACCEPT)
                    elif to_index != -1:
                        if isinstance(symbol, Nonterminal):
                            self.__table[index][symbol] = TableAction(to_index, TableActionEnum.GOTO)
                        # shift
                        elif isinstance(symbol, Terminal):
                            for item in closure.lr0items:
                                if item.is_final_item and symbol in self.__follow.get_follow_of_nonterminal(
                                        item.production_rule.lhs):
                                    raise ShiftReduceConflict(closure, symbol, index)
                            self.__table[index][symbol] = TableAction(to_index, TableActionEnum.SHIFT)

    def parse_sequence(self, buffer):
        buffer.append(Dollar())
        result = []
        stack: Deque[Union[int, Symbol]] = deque([0])
        i = 0
        step = 1
        while i < len(buffer):
            result.append(f"--- STEP {step} ---\n=> STACK STATE: {stack}")
            from_index = stack[-1]
            buffer_symbol = buffer[i]
            action = self.__table[from_index][buffer_symbol]
            if action.state == TableActionEnum.ERROR:
                raise ParsingError(result, f"ERROR: no action found at \
                index: {from_index} with symbol: {buffer_symbol} in the parse_sequence method in the LR1 class.")
            elif action.state == TableActionEnum.ACCEPT:
                result.append(f"END: from {from_index} to ACCEPTED with {buffer_symbol}")
            elif action.state == TableActionEnum.SHIFT:
                result.append(f"SHIFT: from {from_index} to {action.index} with {buffer_symbol}")
                stack.append(buffer_symbol)
                stack.append(action.index)
            elif action.state == TableActionEnum.REDUCE:
                production = self.__grammar.productions[action.index]
                result.append(f"REDUCE: use production {production}")
                if not Epsilon() in production.rhs:
                    for _ in production.rhs:  # pop 2 * len(rhs) items
                        stack.pop()
                        stack.pop()
                step += 1
                from_index = stack[-1]
                stack.append(production.rhs)
                result.append(f"--- STEP {step} ---\n=> STACK STATE: {stack}")
                action = self.__table[from_index][production.lhs]
                result.append(f"GOTO: from {from_index} to {action.index} with {production.lhs}")
                stack.append(action.index)
                i -= 1
            i += 1
            step += 1
        return result
