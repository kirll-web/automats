NAME_POINTS = "Q"
NUMBER_POINTS = 1
SEPARATOR = ";"

class Ptr:
    def __init__(self, value):
        self.value: str = value
        self.next = dict()
        self.prev = dict()


def mealy_transform_to_min(input_file, output_file):
    lines = input_file.readlines()
    mealy_mass = get_mealy_mass(lines)
    mealy_mass = remove_unreacheble_state(mealy_mass)

    for i, line in enumerate(mealy_mass):
        if line == NAME_POINTS:
            output_file.write(";")
        else:
            output_file.write(f"{line};")
        for k, ch in enumerate(mealy_mass[line]):
            if line == NAME_POINTS:
                output_file.write(ch)
                if k < len(mealy_mass[line]) - 1:
                    output_file.write(SEPARATOR)
                continue
            output_file.write(f"${ch[0]}/${ch[1]}")
            if k < len(mealy_mass[line]) - 1:
                output_file.write(SEPARATOR)
        output_file.write("\n")




def remove_unreacheble_state(mealy_mass):
    graph = dict()

    for i, ch in enumerate(mealy_mass[NAME_POINTS]):
        graph[ch] = Ptr(ch)

    for i, new_point in enumerate(mealy_mass[NAME_POINTS]):
        for k, ch in enumerate(mealy_mass):
            if k in range(0, 1):
                continue
            else:
                s = mealy_mass[ch][i]
                if s[0] not in graph: graph[s] = Ptr(s[0])
                graph[new_point].next[s[0]] = graph[s[0]]
                graph[s[0]].prev[new_point] = graph[new_point]

    has_unreach = True
    while has_unreach:
        has_unreach = False
        new_graph = dict()
        for i, ptr in enumerate(graph):
            if ptr != mealy_mass[NAME_POINTS][0] and len(graph[ptr].prev) == 0:
                has_unreach = True
                for b, nextPtr in enumerate(graph[ptr].next):
                    del graph[nextPtr].prev[ptr]
            else:
                new_graph[ptr] = graph[ptr]
        graph = new_graph

    new_mealy_mass = dict()
    new_mealy_mass[NAME_POINTS] = []
    for i, ch in enumerate(mealy_mass[NAME_POINTS]):
        if ch not in graph: continue
        for k, line in enumerate(mealy_mass):
            if line not in new_mealy_mass: new_mealy_mass[line] = list()
            new_mealy_mass[line].append(mealy_mass[line][i])

    return  new_mealy_mass


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