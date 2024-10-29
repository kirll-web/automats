NAME_POINTS = "Q"
NAME_NEW_POINTS = "S"
NAME_OUTPUT_CH = "Y"
NUMBER_OUTPUT_CH = 0
NUMBER_POINTS = 1
SEPARATOR = ";"

reachable_points = dict()

def moore_to_mealy(input_file, output_file):
    lines = input_file.readlines()

    moore_mass = get_moore_mass(lines)
    points_with_transition = dict()

    #составляем переходы
    for i, point in enumerate(moore_mass[NAME_POINTS]):
        points_with_transition[point] = moore_mass[NAME_OUTPUT_CH][i]

    mealy_mass = dict()
    mealy_mass[NAME_POINTS] = []

    unreachable_points_indexes = dict()

    for i, line in enumerate(moore_mass):
        if line == NAME_OUTPUT_CH: continue
        if line == NAME_POINTS:
            for k, point in enumerate(moore_mass[line]):
                if point in reachable_points:
                    mealy_mass[NAME_POINTS].append(point)
                else: unreachable_points_indexes[k] = "" #добавляем индекс недостижимой вершины, чтобы не читать их
            continue

        for b, transition in enumerate(moore_mass[line]):
            if line not in mealy_mass:
                mealy_mass[line] = []
            if b not in unreachable_points_indexes:
                mealy_mass[line].append(f"{transition}/{points_with_transition[transition]}")

    for i, line in enumerate(mealy_mass):
        if line == NAME_POINTS:
            output_file.write(";")
        else: output_file.write(f"{line};")
        for k, ch in enumerate(mealy_mass[line]):
            output_file.write(ch)
            if k < len(mealy_mass[line]) - 1: output_file.write(SEPARATOR)
        output_file.write("\n")


def get_moore_mass(lines):
    mass = dict()
    output_ch_line = lines[NUMBER_OUTPUT_CH]
    points_line = lines[NUMBER_POINTS]

    temp = output_ch_line.strip().split(SEPARATOR)
    mass[NAME_OUTPUT_CH] = []
    for i, item in enumerate(temp):
        if item != "":
         mass[NAME_OUTPUT_CH].append(item)


    temp = points_line.strip().split(SEPARATOR)
    mass[NAME_POINTS] = []
    for i, item in enumerate(temp):
        if item != "":
            mass[NAME_POINTS].append(item)

    for i, line in enumerate(lines):
        if i in range(0,2): continue
        temp = line.strip().split(SEPARATOR)
        mass[temp[0]] = []
        for k, item in enumerate(temp):
            if k != 0:
                mass[temp[0]].append(item)
                reachable_points[item] = ""
    return mass