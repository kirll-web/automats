import sys
OUTPUT_CH = "OUTPUT_CH"
QS = "QS"

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

        for ch in regex:
            if ch == '(':
                operators.append(ch)
            elif ch == ')':
                while operators and operators[-1] != '(':
                    self.process_operator(operators, symbols)
                operators.pop()  # Удалить '('
            elif ch == '|':
                operators.append(ch)

                if len(symbols) > 1:
                    symb2 = symbols.pop()
                    symb1 = symbols.pop()
                    symbols.append(self.nfa_plus_nfa(symb1, symb2))
            elif ch == '*':
                nfa = symbols.pop()
                symbols.append(self.create_kleene_star_nfa(nfa))
            else:
                symbols.append(self.create_symbol_nfa(ch))


        while operators:
            self.process_operator(operators, symbols)

        while len(symbols) > 1:
            symb2 = symbols.pop()
            symb1 = symbols.pop()
            symbols.append(self.nfa_plus_nfa(symb1, symb2))

        return symbols.pop()

    def process_operator(self, operators, operands):
        """Обработать оператор (|, *)."""
        operator = operators.pop()
        if operator == "(":
            operators.append(operator)
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
        regex = "(tw|y)*(tq|t)" #FIXME MOCK
    output_file = open(output_file_name, "w+", encoding="utf-8")
    output_file.close()

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
