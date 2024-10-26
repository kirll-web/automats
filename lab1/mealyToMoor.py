NAME_POINTS = "Q"
NAME_NEW_POINTS = "S"
NAME_OUTPUT_CH = "Y"
NAME_TRANSITION = "QT"
NUMBER_TRANSITION = 0
NUMBER_OUTPUT_CH = 2
NUMBER_POINTS = 1


SEPARATOR = ";"


def mealy_to_moore(input_file, output_file):
    lines = input_file.readlines()
    mealy_mass = get_mealy_mass(lines)
    input_characters, transitions = get_input_characters_with_transitions(mealy_mass)
    offset = 4

    moore_mass = dict()

    moore_mass[NAME_TRANSITION] = []
    moore_mass[NAME_POINTS] = []
    moore_mass[NAME_OUTPUT_CH] = []
    moore_mass[NAME_NEW_POINTS] = []

    for i, (q, t) in enumerate(transitions):
        moore_mass[NAME_TRANSITION].append([q,t])
        moore_mass[NAME_POINTS].append(q)
        moore_mass[NAME_OUTPUT_CH].append(t)
        moore_mass[NAME_NEW_POINTS].append("R" + str(i))

    for i, ch in enumerate(input_characters):
        moore_mass[ch] = []

    for i, line in enumerate(moore_mass):
        if i in range(0, offset): continue
        for k, _ in enumerate(moore_mass[NAME_TRANSITION]):
            moore_q = moore_mass[NAME_POINTS][k]
            moore_input_ch = line
            index = moore_mass[NAME_TRANSITION].index(
                get_q(
                    mealy_mass=mealy_mass,
                    moore_q=moore_q,
                    moore_input_ch=moore_input_ch
                )
            )
            moore_mass[line].append(moore_mass[NAME_NEW_POINTS][index])

    for i, line in enumerate(moore_mass):
        if i in range(0,2): continue
        if i in range(2, 4): output_file.write(SEPARATOR)
        else:
            output_file.write(line)
            output_file.write(SEPARATOR)
        for k, ch in enumerate(moore_mass[line]):
            output_file.write(ch)
            if k < len(moore_mass[line]) - 1: output_file.write(SEPARATOR)
        output_file.write("\n")


def get_q(mealy_mass, moore_q, moore_input_ch):
    i = mealy_mass[NAME_POINTS].index(moore_q)
    q = mealy_mass[moore_input_ch][i]
    return q

def get_mealy_mass(lines):
    mass = dict()
    mass[NAME_POINTS] = []
    temp = lines[0].strip().split(SEPARATOR)
    for i, item in enumerate(temp):
        if item != "": mass[NAME_POINTS].append(item)

    for i, line in enumerate(lines):
        if i == 0: continue
        temp = line.strip().split(SEPARATOR)
        for k, t in enumerate(temp):
            if i > 0 and k > 0:
                temp[k] = t.strip().split("/")
            else: temp[k] = t
        mass[temp[0]] = []
        mass[temp[0]] = temp[1:]
    return mass

def get_input_characters_with_transitions(mass):
    input_characters = []
    transitions = []
    for i, key in enumerate(mass):
        if key_is_system_ch(key): continue
        input_characters.append(key)
        for k, transition in enumerate(mass[key]):
            if transition not in transitions:
                transitions.append(transition)
    return [input_characters,sorted(transitions)]

def key_is_system_ch(key):
    if key in [NAME_NEW_POINTS, NAME_OUTPUT_CH, NAME_POINTS]: return True
    else: return False