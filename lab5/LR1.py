from typing import Dict, List, Set
import re


class Regula:
    def __init__(self, membru_st, membru_dr):
        self.membru_st = membru_st
        self.membru_dr = membru_dr

    def __eq__(self, other):
        if self.membru_dr != other.membru_dr:
            return False
        if self.membru_st != other.membru_st:
            return False
        return True


class Gramatica:
    # def __init__(self, file_name):
    #     self.reguli = []
    #     with open(file_name) as file:
    #         lines = file.readlines()
    #         for line in lines:
    #             line = line.strip()
    #             membrii = line.split()
    #             self.reguli.append(Regula(membrii[0], membrii[1]))

    def __init__(self, lista_reguli):
        self.reguli = lista_reguli

    def reguli_cu_neterminal(self, neterminal):
        reguli = []
        for regula in self.reguli:
            if regula.membru_st == neterminal:
                reguli.append(regula)
        return reguli


class ElementStare:
    def __init__(self, membru_st, membru_dr, pozitie_punct, predictie):
        self.membru_st = membru_st  # string
        self.membru_dr = membru_dr  # string
        self.pozitie_punct = pozitie_punct  # integer in interval inchis [0, len(membru_dr)] TODO: verificare daca egal cu len(pozitie_punct)
        self.predictie = predictie  # lista de caractere (luate din tabelul FIRST1)

    def to_string(self):
        membru_dr_string = ""
        for index, char in enumerate(self.membru_dr):
            if index == self.pozitie_punct:
                membru_dr_string += "."
            membru_dr_string += char
        predictie_string = ""
        for index, el_pred in enumerate(self.predictie):
            predictie_string += el_pred
            if index != len(self.predictie) - 1:
                predictie_string += "/"
        if predictie_string == "":
            predictie_string = "$"
        return "[" + self.membru_st + "->" + membru_dr_string + "," + predictie_string + "]"

    def __eq__(self, other):
        if self.membru_dr != other.membru_dr:
            return False
        if self.membru_st != other.membru_st:
            return False
        if self.pozitie_punct != other.pozitie_punct:
            return False
        if self.predictie != other.predictie:
            return False
        return True


class Stare:
    def __init__(self, index, elemente_initiale, gramatica, tabel_first1):  # Closure se face aici
        # index: int - numarul starii
        # element_initial: ElementStare - elementul de analiza initial, peste care se va face Closure
        # gramatica: Gramatica
        # tabel_first1: dictionar: neterminal -> lista[terminal1, ...] - FIRST1 pentru fiecare neterminal din gramatica
        self.index = index
        self.elemente = elemente_initiale
        self.neterminale_verificate = []
        done = False
        while not done:
            done = True
            for element in self.elemente:
                membru_dr = element.membru_dr
                membru_st = element.membru_st
                pozitie_punct = element.pozitie_punct
                # if membru_st[0] in membru_dr and pozitie_punct+1<len(membru_dr):
                #     for pred in tabel_first1[membru_dr[pozitie_punct+1]]:
                #         if pred not in element.predictie:
                #             element.predictie += pred
                # if element.membru_st == "B":
                #     element.predictie += 'c'
                # if self.index == 48:
                #     print(element.to_string())

                if pozitie_punct >= len(membru_dr):
                    continue
                if membru_dr[pozitie_punct].isupper() and membru_dr[pozitie_punct] not in self.neterminale_verificate:
                    reguli_cu_neterminal = gramatica.reguli_cu_neterminal(membru_dr[pozitie_punct])
                    self.neterminale_verificate.append(membru_dr[pozitie_punct])
                    for regula in reguli_cu_neterminal:
                        # predictie = [] # ???? TODO
                        # # I 48 :
                        # # [A->#include<iostream>usingnamespacestd;voidmain(){.B},$]
                        # # [B->.C,}]
                        # # [B->.BC,}] -> B ar mai trebui desfacut aici inca o data pentru a include FIRST1 de la C
                        # if regula.membru_st in regula.membru_dr:
                        #     try:
                        #         predictie += tabel_first1[regula.membru_dr[regula.membru_dr.index(regula.membru_st)+1]]
                        #     except KeyError:
                        #         predictie += [regula.membru_dr[regula.membru_dr.index(regula.membru_st)+1]]
                        #     except IndexError:
                        #         pass
                        try:
                            self.elemente.append(ElementStare(regula.membru_st, regula.membru_dr, 0,
                                                              element.predictie + tabel_first1[
                                                                  membru_dr[pozitie_punct + 1]]))
                        except IndexError:
                            self.elemente.append(ElementStare(regula.membru_st, regula.membru_dr, 0, element.predictie))
                        except KeyError:
                            if membru_dr[pozitie_punct + 1] not in element.predictie:
                                self.elemente.append(ElementStare(regula.membru_st, regula.membru_dr, 0,
                                                                  element.predictie + [membru_dr[pozitie_punct + 1]]))
                    done = False

    def to_string(self):
        to_string = ""
        for element in self.elemente:
            to_string += element.to_string() + "\n"
        return to_string

    def __eq__(self, other):
        sorted_elements = sorted(self.elemente, key=lambda x: (x.membru_st, x.membru_dr))
        sorted_other_elements = sorted(other.elemente, key=lambda x: (x.membru_st, x.membru_dr))
        if len(sorted_elements) != len(sorted_other_elements):
            return False
        for index in range(len(sorted_elements)):
            if sorted_elements[index] != sorted_other_elements[index]:
                return False
        return True


class ColectieCanonica:
    def __init__(self, gramatica, tabel_first1, ter_net):  # Goto se face aici
        regula_noua = Regula("Z", gramatica.reguli[0].membru_st)
        gramatica.reguli.insert(0, regula_noua)
        self.count_stari = 0
        self.stari = [
            Stare(self.count_stari, [ElementStare(regula_noua.membru_st, regula_noua.membru_dr, 0, [])], gramatica,
                  tabel_first1)]
        done = False
        self.count_stari += 1
        self.graf = []
        while not done:
            done = True
            for stare in self.stari:
                for t_n in ter_net:
                    elemente_initiale_stare_noua = []
                    for element in stare.elemente:
                        if element.pozitie_punct >= len(element.membru_dr):
                            continue
                        if element.membru_dr[element.pozitie_punct] == t_n:
                            elemente_initiale_stare_noua.append(
                                ElementStare(element.membru_st, element.membru_dr, element.pozitie_punct + 1,
                                             element.predictie))
                    if len(elemente_initiale_stare_noua) > 0:
                        stare_noua = Stare(self.count_stari, elemente_initiale_stare_noua, gramatica, tabel_first1)
                        if stare_noua == stare and (stare.index, t_n, stare.index) not in self.graf:
                            self.graf.append((stare.index, t_n, stare.index))
                        if stare_noua in self.stari and (
                        stare.index, t_n, self.stari[self.stari.index(stare_noua)].index) not in self.graf:
                            self.graf.append((stare.index, t_n, self.stari[self.stari.index(stare_noua)].index))
                        if stare_noua not in self.stari:
                            done = False
                            self.stari.append(stare_noua)
                            self.count_stari += 1
                            self.graf.append((stare.index, t_n, stare_noua.index))

    def print(self):
        print(self.graf)
        for stare in self.stari:
            print("I", stare.index, ":")
            print(stare.to_string())


class TabelAnaliza:
    def __init__(self, gramatica, colectie_canonica):
        self.tabel = []
        for _ in range(colectie_canonica.count_stari):
            self.tabel.append({})
        for muchie in colectie_canonica.graf:
            self.tabel[muchie[0]][muchie[1]] = "s" + str(muchie[2])
        for stare in colectie_canonica.stari:
            # if len(stare.elemente) == 1:
            if len(stare.elemente[0].predictie) == 0:
                if stare.elemente[0].membru_st == "Z":
                    self.tabel[stare.index]["$"] = "acc"
                else:
                    self.tabel[stare.index]["$"] = "r" + str(
                        gramatica.reguli.index(Regula(stare.elemente[0].membru_st, stare.elemente[0].membru_dr)))
            else:
                for pred in stare.elemente[0].predictie:
                    self.tabel[stare.index][pred] = "r" + str(
                        gramatica.reguli.index(Regula(stare.elemente[0].membru_st, stare.elemente[0].membru_dr)))
                self.tabel[stare.index]["c"] = "r" + str(
                    gramatica.reguli.index(Regula(stare.elemente[0].membru_st, stare.elemente[0].membru_dr)))
                # self.tabel[stare.index]["a"] = "r"+str(gramatica.reguli.index(Regula(stare.elemente[0].membru_st, stare.elemente[0].membru_dr)))
                if stare.elemente[0].membru_st in "BCDEFGHI":
                    for letter in "qwertyuiopasdfghjklzxcvbnm":
                        try:
                            self.tabel[stare.index][letter]
                        except KeyError:
                            self.tabel[stare.index][letter] = "r" + str(gramatica.reguli.index(
                                Regula(stare.elemente[0].membru_st, stare.elemente[0].membru_dr)))
                if stare.elemente[0].membru_st in "KLMO":
                    for operator in "*-+!=>":
                        try:
                            self.tabel[stare.index][operator]
                        except KeyError:
                            self.tabel[stare.index][operator] = "r" + str(gramatica.reguli.index(
                                Regula(stare.elemente[0].membru_st, stare.elemente[0].membru_dr)))
                if stare.elemente[0].membru_st in "OQ":
                    for num in "1234567890":
                        try:
                            self.tabel[stare.index][num]
                        except KeyError:
                            self.tabel[stare.index][num] = "r" + str(gramatica.reguli.index(
                                Regula(stare.elemente[0].membru_st, stare.elemente[0].membru_dr)))
                if stare.elemente[0].membru_st in "BCDEFGHIOTRP":
                    try:
                        self.tabel[stare.index][";"]
                    except KeyError:
                        self.tabel[stare.index][";"] = "r" + str(
                            gramatica.reguli.index(Regula(stare.elemente[0].membru_st, stare.elemente[0].membru_dr)))

    def print(self):
        print(self.tabel)


def terminali_neterminali(gramatica):  # toti terminalii si neterminalii din gramatica neimbogatita
    ter_net = []
    for regula in gramatica.reguli:
        for char in regula.membru_st:
            if char not in ter_net:
                ter_net.append(char)
        for char in regula.membru_dr:
            if char not in ter_net:
                ter_net.append(char)
    return ter_net


def analiza_secventa(secventa, tabel_analiza, gramatica):
    stiva = "0"
    index_secventa = 0
    secventa += "$"
    istorie = ""
    while index_secventa < len(secventa):
        index_stiva2 = len(stiva) - 1
        string_stare = ""
        while stiva[index_stiva2].isdigit() and index_stiva2 >= 0:
            if stiva[index_stiva2 - 1] == '\\':
                break
            string_stare = stiva[index_stiva2] + string_stare
            index_stiva2 -= 1
        index_stare = int(string_stare)
        try:
            actiune = tabel_analiza.tabel[index_stare][secventa[index_secventa]]
        except KeyError:
            print(stiva, index_stare, secventa[index_secventa], "err")
            break
        print(stiva, secventa[index_secventa:], istorie, actiune)
        if actiune == "acc":
            break
        if actiune[0] == "s":
            if secventa[index_secventa].isdigit():
                stiva += '\\'
            stiva += secventa[index_secventa] + actiune[1:]
            index_secventa += 1
        if actiune[0] == "r":
            index_stiva = len(stiva)
            regula = gramatica.reguli[int(actiune[1:])]
            found = secventa[index_secventa] in regula.membru_dr
            if found and secventa[index_secventa] != 'c':
                reduce = secventa[index_secventa]
            else:
                reduce = ""
            print(regula.membru_st, '->', regula.membru_dr)
            if not regula.membru_dr[0].isdigit():
                # print(stiva)
                while reduce != regula.membru_dr:
                    # print(reduce)
                    index_stiva -= 1
                    # print(index_stiva)
                    # print(stiva)
                    if not stiva[index_stiva].isdigit() and stiva[index_stiva] != '\\':
                        reduce = stiva[index_stiva] + reduce
            else:
                while reduce != regula.membru_dr:
                    # print(reduce)
                    index_stiva -= 1
                    # print(index_stiva)
                    if stiva[index_stiva].isdigit() and stiva[index_stiva - 1] == '\\':
                        reduce = stiva[index_stiva] + reduce
            if stiva[index_stiva - 1] != '\\':
                stiva = stiva[:index_stiva] + regula.membru_st
            else:
                stiva = stiva[:index_stiva - 1] + regula.membru_st
            # print(stiva)
            index_stiva3 = len(stiva) - 2
            string_stare2 = ""
            while stiva[index_stiva3].isdigit() and index_stiva3 >= 0:
                string_stare2 = stiva[index_stiva3] + string_stare2
                index_stiva3 -= 1
            index_stare2 = int(string_stare2)
            stiva += tabel_analiza.tabel[index_stare2][stiva[len(stiva) - 1]][1:]
            # print(stiva)
            if found:
                index_secventa += 1


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


class Dollar(Symbol):
    def __init__(self):
        super(Dollar, self).__init__("$")
        self.__dollar = "$"

    @staticmethod
    def check_symbol(s: str) -> bool:
        return s == "$"


class Epsilon(Symbol):
    def __init__(self):
        super(Epsilon, self).__init__("epsilon")
        self.__dollar = "epsilon"

    @staticmethod
    def check_symbol(s: str) -> bool:
        return s == "epsilon"


class Nonterminal(Symbol):
    def __init__(self, symbol):
        super(Nonterminal, self).__init__(symbol)
        self.__nonterminal = "NONTERMINAL"

    @staticmethod
    def check_symbol(s: str) -> bool:
        return re.match("[A-Z_']+", s) is not None and s.isupper()

    def __repr__(self):
        return f'T:{self._symbol}'


class Terminal(Symbol):
    def __init__(self, symbol):
        super(Terminal, self).__init__(symbol)
        self.__terminal = "TERMINAL"

    @staticmethod
    def check_symbol(s: str) -> bool:
        return re.match('[^A-Z]+', s) is not None  # and s.islower()

    def __repr__(self):
        return f"t:{self._symbol}"


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

    def to_gramatica(self):
        reguli = []
        for production in self.__productions:
            membru_st = production.lhs.symbol
            membru_dr = ""
            for x in production.rhs:
                membru_dr += x.symbol
            regula = Regula(membru_st, membru_dr)
            reguli.append(regula)
            # print(regula.membru_st, regula.membru_dr)
        return Gramatica(reguli)

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


class First:
    def __init__(self, grammar: Grammar):
        self.__grammar = grammar
        self.__first: Dict[Nonterminal, Set[Symbol]] = {}
        self.find_first()

    def to_py_dict(self):
        py_dict = {}
        for key, value in self.__first.items():
            py_dict[key.symbol] = [symbol._symbol for symbol in list(value)]
        # print(py_dict)
        return py_dict

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


def read_grammar(path):
    nonterminals = set()
    terminals = set()
    productions = []
    with open(path) as fin:
        for line in fin:
            line = line.strip().rstrip()
            if line:
                lhs, rhs = line.split('->')

                lhs_nonterminal = Nonterminal(lhs)
                nonterminals.add(lhs_nonterminal)
                rhs = rhs.split('|')
                for rhs_ in rhs:
                    rhs_ = rhs_.split(' ')
                    rhs_list = []
                    for rhs__ in rhs_:
                        if Epsilon.check_symbol(rhs__):
                            rhs_list.append(Epsilon())
                        elif Nonterminal.check_symbol(rhs__):
                            nonterminal = Nonterminal(rhs__)
                            nonterminals.add(nonterminal)
                            rhs_list.append(nonterminal)
                        elif Terminal.check_symbol(rhs__):
                            terminal = Terminal(rhs__)
                            terminals.add(terminal)
                            rhs_list.append(terminal)
                    productions.append(Production(lhs_nonterminal, rhs_list))

    ter_net = []
    for terminal in list(terminals):
        ter_net.append(terminal.symbol)
    for neterminal in list(nonterminals):
        ter_net.append(neterminal.symbol)
    return Grammar(list(terminals), list(nonterminals), productions), ter_net


def fip_to_string(fip, fip_map):
    program_string = ""
    for element in fip:
        if isinstance(element, tuple):
            program_string += element[1]
        else:
            program_string += fip_map[element]
    return program_string


grammar, ter_net = read_grammar("mlp_grammar.txt")
# print(ter_net)
first = First(grammar)
tabel_first1 = first.to_py_dict()
gramatica = grammar.to_gramatica()

# gramatica = Gramatica('gramatica.txt')
# ter_net = terminali_neterminali(gramatica)
# print(ter_net)
# tabel_first1 = {"Z":["a","b"], "S":["a","b"], "A":["a","b"]}
colectie_canonica = ColectieCanonica(gramatica, tabel_first1, ter_net)
tabel_analiza = TabelAnaliza(gramatica, colectie_canonica)

# colectie_canonica.print()
# tabel_analiza.print()
# print(tabel_first1)

fip_map = {
    0: "const",
    1: "id",
    2: "if",
    3: "else",
    4: "while",
    5: "cout",
    6: ">>",
    7: "int",
    8: "<<",
    9: "#",
    10: ")",
    11: "(",
    12: "+",
    13: "namespace",
    14: ";",
    15: "main",
    16: "=",
    17: "<",
    18: ">",
    19: "iostream",
    20: "void",
    21: "using",
    22: "endl",
    23: "std",
    24: "include",
    25: "cin",
    26: "{",
    27: "}",
    28: "*",
    29: "-",
    30: "!=",
    31: "char",
    32: "circle"
}

fip = [9, 24, 17, 19, 18, 21, 13, 23, 14, 20, 15, 11, 10, 26, 7, (1, "a"), 14, 25, 6, (1, "a"), 14, (1, "a"), 16,
       (1, "a"), 12, (0, "1"), 14, 5, 8, (1, "a"), 8, 22, 14, 27]
fip_error = [9, 24, 17, 19, 18, 21, 13, 23, 14, 20, 15, 11, 10, 7, (1, "a"), 14, 25, 6, (1, "a"), 14, (1, "a"), 16,
             (1, "a"), 12, (0, "1"), 14, 5, 8, (1, "a"), 8, 22, 14, 27]

program_string = fip_to_string(fip_error, fip_map)
print(program_string)

analiza_secventa(program_string, tabel_analiza, gramatica)
