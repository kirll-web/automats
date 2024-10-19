def mealy_to_moore(input_file, output_file):
    lines = input_file.readlines()
    mealy_mass = get_mealy_mass(lines)
    input_characters, transitions = get_input_characters_with_transitions(mealy_mass)
    offset = 4
    moore_mass = [[] for _ in range(len(lines) + offset - 1)]

    moore_mass[0].append("")
    moore_mass[1].append("")
    moore_mass[2].append("")
    moore_mass[3].append("")

    for i, (q, t) in enumerate(transitions):
        moore_mass[0].append([q,t])
        moore_mass[1].append(q)
        moore_mass[2].append(t)
        moore_mass[3].append("R" + str(i))

    for i, ch in enumerate(input_characters):
        moore_mass[i+offset].append(ch)
        for _ in moore_mass[0][1:]:
            moore_mass[i+offset].append("")


    for i, line in enumerate(moore_mass):
        if i in range(0, offset): continue
        for k, _ in enumerate(line):
            if k == 0: continue
            moore_q = moore_mass[1][k]
            moore_input_ch = line[0]
            moore_mass[i][k] = get_q(
                    mealy_mass=mealy_mass,
                    moore_mass=moore_mass,
                    moore_q=moore_q,
                    moore_input_ch=moore_input_ch
                )

    for i, line in enumerate(moore_mass):
        if i in range(0, offset): continue
        for k, _ in enumerate(line):
            if k == 0: continue
            moore_q = moore_mass[1][k]
            moore_input_ch = line[0]
            index = moore_mass[0].index(
                get_q(
                    mealy_mass=mealy_mass,
                    moore_mass=moore_mass,
                    moore_q=moore_q,
                    moore_input_ch=moore_input_ch
                )
            )
            moore_mass[i][k] = moore_mass[3][index]

    for i, line in enumerate(moore_mass):
        if i in range(0,2): continue
        for k, ch in enumerate(line):
            output_file.write(ch)
            if k < len(line) - 1: output_file.write(";")
        output_file.write("\n")


def get_q(mealy_mass, moore_mass, moore_q, moore_input_ch):
    i = mealy_mass[0].index(moore_q)

    k = 0
    for b, c in enumerate(mealy_mass): # todo проблема в нахождении k
        if moore_input_ch == c[0]:
            k = b; break

    q = mealy_mass[k][i]
    return q

def get_mealy_mass(lines):
    mass = [[] for _ in range(len(lines))]
    for i, line in enumerate(lines):
        temp = line.strip().split(";")
        for k, t in enumerate(temp):
            if i > 0 and k > 0:
                temp[k] = t.strip().split("/")
            else: temp[k] = t
        mass[i] = temp
    return mass

def get_input_characters_with_transitions(mass):
    input_characters = []
    transitions = []
    for i, line in enumerate(mass):
        if i == 0: continue
        input_characters.append(line[0])
        for k, transition in enumerate(line):
            if k == 0: continue
            if transition not in transitions:
                transitions.append(transition)
    return [input_characters,sorted(transitions)]

