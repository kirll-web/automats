import sys

from moore import moore_transform_to_min

LINE_END = "LINE_END"
LINE_STATES = "LINE_STATES"
LINE_CH = "LINE_CH"
EMPTY_CH = "ε"
NAME_END = "F"
Q_SEPARATOR = ","
NAME_NEW_Q = "S"
end_state = "null"


def mockOutput(table):
    for i, b in enumerate(table):
        print(i, b, table[b])

def read_nfa(input_file):
    global end_state
    lines = input_file.readlines()
    automat = dict()
    automat[LINE_END] = []
    automat[LINE_STATES] = []
    index_end_state = 0
    for index, line in enumerate(lines):
        if index == 0:
            for i, ch in enumerate(line.strip().split(";")):
                if i != 0: automat[LINE_END].append(ch)
                if ch == NAME_END:
                    index_end_state = i
        else:
            if index == 1:
                for i, ch in enumerate(line.strip().split(";")):
                    if i != 0: automat[LINE_STATES].append(ch)
                    if i == index_end_state: end_state = ch
            else:
                first_ch = line.strip().split(";")[0]
                for i, ch in enumerate(line.strip().split(";")):
                    if i == 0: automat[first_ch] = []
                    else: automat[first_ch].append(ch)
    return automat

def determinate(nfa_automat, output_file):
    empty_transitions = dict()

    for index, ch in enumerate(nfa_automat[LINE_STATES]):
        empty_transitions[ch] = []
        empty_transitions[ch].append(ch)
        empty_tr = nfa_automat[EMPTY_CH][index]
        if empty_tr != "":
            empty_tr = empty_tr.split(Q_SEPARATOR)
            for tr in empty_tr:
                if tr != "":
                    if tr not in empty_transitions[ch]: empty_transitions[ch].append(tr)
                    for i in empty_transitions:
                        if ch in empty_transitions[i] and tr not in empty_transitions[i]:
                            empty_transitions[i].append(tr)
    table = dict()
    table[LINE_CH] = []

    for ch in nfa_automat:
        if ch == LINE_END or ch == LINE_STATES or ch == EMPTY_CH: continue
        table[LINE_CH].append(ch)
    start_q = list(empty_transitions.items())[0][1]
    start_q =  Q_SEPARATOR.join(map(str, start_q))
    print(start_q)
    table[start_q] = []
    
    find_new_q = True
    finded_q = dict()
    finded_q[start_q] = False
    while find_new_q:
        find_new_q = False
        new_finded_q = finded_q.copy()
        for index, item in enumerate(finded_q):
            if finded_q[item]: continue
            table[item] = []
            for i in range(0, len(table[LINE_CH])):
                table[item].append("") #заполнение массива пустыми массивами == количеству LINE_CH
            qs = item.split(Q_SEPARATOR)
            if len(qs) > 1:
                for q in qs:
                    for kindex, ch in enumerate(table[LINE_CH]):
                        if ch == EMPTY_CH: continue
                        c = ch
                        tr = nfa_automat[c][nfa_automat[LINE_STATES].index(q)]
                        if tr != "":
                            new_tr = tr
                            if len(table[item][kindex]) > 0:
                                new_tr = f"{table[item][kindex]},{tr}"
                            table[item][kindex] = new_tr

                            if new_tr not in finded_q:
                                new_finded_q[new_tr] = False
                                find_new_q = True
            # этот переход нам нужно подставить в строчку table[item] в столбце под нужным симвлом
            # в конце подстановки нужно добавить все новые перехоы в finded_q. Если найдены новые переходы
            # find_new_q = True
            # иначе False
            else:
                q = qs[0]
                for kindex, ch in enumerate(table[LINE_CH]):
                    if ch == EMPTY_CH: continue
                    tr = nfa_automat[ch][nfa_automat[LINE_STATES].index(q)]
                    if tr != "":
                        new_tr = tr
                        if len(table[item][kindex]) > 0:
                            new_tr = f"{table[item][kindex]},{tr}"
                        table[item][kindex] = new_tr

                        if new_tr not in finded_q:
                            new_finded_q[new_tr] = False
                            find_new_q = True
            new_finded_q[item] = True
        finded_q = new_finded_q

    rewrite_table = dict()
    rewrite_table[LINE_END] = []
    rewrite_table[LINE_STATES] = dict()

    for yandex, line in enumerate(table):
        if line == LINE_CH:
            for kindex, ch in enumerate(table[LINE_CH]):
                rewrite_table[ch] = []
                for i in range(1, len(table)):
                    rewrite_table[ch].append("")
        else:
            rewrite_table[LINE_STATES][line] = f"{NAME_NEW_Q}{yandex}"
    for yandex in range(0, len(rewrite_table[LINE_STATES])):
        if yandex < len(rewrite_table[LINE_STATES]) - 1: rewrite_table[LINE_END].append(";")
        else:  rewrite_table[LINE_END].append(NAME_END)

    for yandex, ch in enumerate(table[LINE_CH]):
        for kindex, q in enumerate(table):
            if q == LINE_CH: continue
            s = table[q][yandex]
            if s == "": rewrite_table[ch][kindex-1] = s
            else: rewrite_table[ch][kindex-1] = rewrite_table[LINE_STATES][s]

    for i, b in enumerate(rewrite_table):
        if b == LINE_END:
            print(";", end = "")
            for k, c in enumerate(rewrite_table[b]):
                print(f"{c}", end ="")
            print()
        else:
            if b == LINE_STATES:
                for k, c in enumerate(rewrite_table[b]):
                    print(f";{rewrite_table[b][c]}", end ="")
                print()
            else:
                print(b, end="")
                for k, c in enumerate(rewrite_table[b]):
                    print(f";{c}", end="")
                print()


    temp_file = open("temp.csv", "w+", encoding="utf-8")
    for i, b in enumerate(rewrite_table):
        if b == LINE_END:
            temp_file.write(";")
            for k, c in enumerate(rewrite_table[b]):
                temp_file.write(c)
            temp_file.write("\n")
        else:
            if b == LINE_STATES:
                for k, c in enumerate(rewrite_table[b]):
                    temp_file.write(f";{rewrite_table[b][c]}")
                temp_file.write("\n")
            else:
                temp_file.write(b)
                for k, c in enumerate(rewrite_table[b]):
                    temp_file.write(f";{c}")
                temp_file.write("\n")

    temp_file.close()
    temp_file =  open("temp.csv", "r", encoding="utf-8")
    moore_transform_to_min(temp_file, output_file)

    

def main(args):
    input_file_name = args[0]
    output_file_name = args[1]
    #input_file_name = "3.csv"
    #output_file_name = "output.csv"
    input_file = open(input_file_name, "r",  encoding="utf-8")
    output_file = open(output_file_name, "w+", encoding="utf-8")

    nfa_automat = read_nfa(input_file)

    determinate(nfa_automat, output_file_name)

    output_file.close()

if __name__ == '__main__':
    main(sys.argv[1:])