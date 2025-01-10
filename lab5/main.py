import sys
OUTPUT_CH = "OUTPUT_CH"
QS = "QS"

OPERATORS = ["(",")", "|"]

class State:
    def __init__(self, id):
        self.id = id
        self.transitions = {}  # {symbol: [state1, state2, ...]}

class NFA:
    def __init__(self, start_state, accept_state):
        self.start_state = start_state
        self.accept_state = accept_state

class RegexToNFA:
    def __init__(self):
        self.state_counter = 0

    def create_state(self):
        """Создать новое состояние с уникальным идентификатором."""
        state = State(self.state_counter)
        self.state_counter += 1
        return state

    def create_symbol_nfa(self, symbol):
        """Создать НКА для одного символа."""
        start = self.create_state()
        accept = self.create_state()
        start.transitions[symbol] = [accept]
        return NFA(start, accept)

    def create_union_nfa(self, left, right):
        """Создать НКА для операции '|'."""
        start = self.create_state()
        accept = self.create_state()
        start.transitions[None] = [left.start_state, right.start_state]  # Пустые переходы
        left.accept_state.transitions[None] = [accept]
        right.accept_state.transitions[None] = [accept]
        return NFA(start, accept)

    def create_kleene_star_nfa(self, nfa):
        """Создать НКА для операции '*'."""
        start = self.create_state()
        medium = self.create_state()
        accept = self.create_state()
        start.transitions[None] = [medium]  # Пустые переходы
        medium.transitions[None] = [nfa.start_state, accept]
        nfa.accept_state.transitions[None] = [medium]
        return NFA(start, accept)

    def create_plus_nfa(self, nfa):
        """Создать НКА для операции '*'."""
        start = self.create_state()
        accept = self.create_state()
        start.transitions[None] = [nfa.start_state]  # Пустые переходы
        nfa.accept_state.transitions[None] = [nfa.start_state, accept]
        return NFA(start, accept)

    def nfa_plus_nfa(self, nfa1: NFA, nfa2: NFA):
        """Создать НКА для операции '*'."""
        start = self.create_state()
        accept = self.create_state()
        nfa1.accept_state.transitions[None] = [nfa2.start_state]  # Пустые переходы
        nfa2.accept_state.transitions[None] = [accept]
        start.transitions[None] = [nfa1.start_state]
        return NFA(start, accept)

    def build_nfa(self, regex):
        """Построить НКА из регулярного выражения."""
        operators = []
        symbols = []
        free_symbols = 0

        for ch in regex:
            if ch == '(':
                operators.append(ch)
            elif ch == ')':
                while operators and operators[-1] != "(":
                    operator = operators.pop()
                    self.process_operator(operators, symbols, operator)
                while free_symbols > 1:
                    symb2 = symbols.pop()
                    symb1 = symbols.pop()
                    symbols.append(self.nfa_plus_nfa(symb1, symb2))
                    free_symbols -= 1
                operators.pop()
                free_symbols = 0

            elif ch == '|':
                while free_symbols > 1:
                    symb2 = symbols.pop()
                    symb1 = symbols.pop()
                    symbols.append(self.nfa_plus_nfa(symb1, symb2))
                    free_symbols -= 1
                free_symbols = 0
                operators.append(ch)


            elif ch == '*':
                nfa = symbols.pop()
                symbols.append(self.create_kleene_star_nfa(nfa))
            elif ch == '+':
                nfa = symbols.pop()
                symbols.append(self.create_plus_nfa(nfa))

            else:
                symbols.append(self.create_symbol_nfa(ch))
                free_symbols += 1


        while operators:
            operator = operators.pop()
            if operator == "|":
                end_symb = symbols.pop()
                while len(symbols) > 1:
                    symb2 = symbols.pop()
                    symb1 = symbols.pop()
                    symbols.append(self.nfa_plus_nfa(symb1, symb2))
                symbols.append(end_symb)
            self.process_operator(operators, symbols, operator)

        while len(symbols) > 1:
            symb2 = symbols.pop()
            symb1 = symbols.pop()
            symbols.append(self.nfa_plus_nfa(symb1, symb2))

        return symbols.pop()

    def process_operator(self, operators, operands, operator):
        """Обработать оператор (|, *)."""
        if operator == "(":
            operators.append("(")
        if operator == '|':
            right = operands.pop()
            left = operands.pop()
            operands.append(self.create_union_nfa(left, right))
        elif operator == '*':
            nfa = operands.pop()
            operands.append(self.create_kleene_star_nfa(nfa))

def is_kleen_star_next(regex, i_ch):
    if i_ch < len(regex) - 1:
        if regex[i_ch] == "*":
            return True
    return False

def main(args):
    output_file_name = ""
    regex = ""
    try:
        output_file_name = args[0]
        regex = args[1]
    except Exception:
        output_file_name = "output.csv"
        regex = "((wwε*t|wte)(((eε*t)|ε))*r|wteq)((t(wwε*t|wte)|(qte|r))(((eε*t)|ε))*r|(twteq|qteq))*tt|t" #FIXME MOCK
    output_file = open(output_file_name, "w+", encoding="utf-8")
    output_file.close()


    literals = []
    buffer = []
    for i_ch, ch in enumerate(regex):
        if (ch == "*" or ch == "+") and len(literals) == 0:
            buffer.append(ch)
        elif ch not in OPERATORS:
            literals.append(ch)
        else:
            if len(literals) > 0:
                buffer.append(f'({"".join(literals)})')
                literals.clear()
            buffer.append(ch)
    if len(literals) > 0:
        buffer.append(f'({"".join(literals)})')
        literals.clear()
    print(regex)
    regex = "".join(buffer)
    print(regex)

    converter = RegexToNFA()
    nfa = converter.build_nfa(regex)

    def print_nfa(nfa):
        visited = set()
        stack = [nfa.start_state]

        print("Состояния и переходы:")
        while stack:
            state = stack.pop()
            if state.id in visited:
                continue
            visited.add(state.id)
            for symbol, targets in state.transitions.items():
                symbol_str = symbol if symbol is not None else "ε"
                for target in targets:
                    print(f"State {state.id} --{symbol_str}--> State {target.id}")
                    stack.append(target)
    with open(output_file_name, 'w', newline='', encoding='utf-8') as file:
        # проверяем какое стартовое состояние и записываем сначала его
        output_dict = dict()
        output_dict[OUTPUT_CH] = []
        output_dict[QS] = []

        #output_dict[OUTPUT_CH].append(";")
        output_dict[QS].append(nfa.start_state.id)

        visited = set()
        end = nfa.accept_state
        output_dict[QS].append(end.id)
        output_dict[OUTPUT_CH].append(""),
        output_dict[OUTPUT_CH].append("F")
        stack = [nfa.start_state]
        max_size = 1
        while stack:
            state = stack.pop()
            if state.id in visited:
                continue
            visited.add(state.id)
            for symbol, targets in state.transitions.items():
                symbol_str = symbol if symbol is not None else "ε"
                for target in targets:
                    if symbol_str not in output_dict:
                        output_dict[symbol_str] = []
                    if state.id not in output_dict[QS]:
                        output_dict[QS].append(state.id)
                        if state.id == end.id:
                            output_dict[OUTPUT_CH].append("F")
                        else:
                            output_dict[OUTPUT_CH].append("")
                    state_index = output_dict[QS].index(state.id)
                    if max_size <= state_index: max_size = state_index + 1
                    print()
                    if len(output_dict[symbol_str]) <= max_size:
                        for item in output_dict:
                            if item == QS or item == OUTPUT_CH: continue
                            if len(output_dict[item]) < max_size:
                                for i in range(len(output_dict[item]), max_size):
                                    output_dict[item].append("")
                    print(len(output_dict[symbol_str]), max_size, state_index)
                    if len(output_dict[symbol_str][state_index]) == 0:
                        output_dict[symbol_str][state_index] = f"{target.id}"
                    else: output_dict[symbol_str][state_index] += f",{target.id}"
                    print(f"State {state.id} --{symbol_str}--> State {target.id}")
                    stack.append(target)

        for symbol in output_dict:
            if symbol == QS or symbol == OUTPUT_CH: continue
            if len(output_dict[symbol]) < len(output_dict[QS]):
                for i in range(len(output_dict[symbol]), len(output_dict[QS])):
                    output_dict[item].append("")


        for item in output_dict:
            # if item == OUTPUT_CH:
            #     file.write(";")
            if item != QS and item != OUTPUT_CH:
                file.write(f"{item}")
            for k in output_dict[item]:
                file.write(f";{k}")
            file.write("\n")


if __name__ == "__main__":
    main(sys.argv[1:])
