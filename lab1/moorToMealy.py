NAME_POINTS = "Q"
NAME_NEW_POINTS = "S"
NAME_OUTPUT_CH = "Y"
NUMBER_OUTPUT_CH = 0
NUMBER_POINTS = 1
SEPARATOR = ";"

def moore_to_mealy(input_file, output_file):
    lines = input_file.readlines()

    moore_mass = get_moore_mass(lines)
    points = add_points(moore_mass)
    input_characters = get_input_characters(moore_mass)
    mealy_mass = create_mealy(input_characters, points)

    last_item = ""
    for i, item in enumerate(moore_mass[NAME_NEW_POINTS]):
        if last_item == item: continue
        last_item = item
        for k, key in enumerate(moore_mass) :
            if key_is_system_ch(key): continue
            old_point = moore_mass[key][i]

            index = moore_mass[NAME_POINTS].index(old_point)
            new_moore_point = moore_mass[NAME_NEW_POINTS][index]
            moore_output_ch = moore_mass[NAME_OUTPUT_CH][index]

            mealy_mass[key][i] = new_moore_point + "/" + moore_output_ch

    output_file.write(SEPARATOR)
    for k, point in enumerate(mealy_mass[NAME_NEW_POINTS]):
        output_file.write(point)
        if k < len(mealy_mass[NAME_NEW_POINTS]) - 1: output_file.write(SEPARATOR)
    output_file.write("\n")
    for i, key in enumerate(mealy_mass):
        if i == 0: continue
        output_file.write(key)
        output_file.write(SEPARATOR)
        for k, ch in enumerate(mealy_mass[key]):
            output_file.write(ch)
            if k < len(mealy_mass[key]) - 1: output_file.write(";")
        output_file.write("\n")


    for i, line in enumerate(mealy_mass):
        print(line)

def create_mealy(input_characters, points):
    line_number = 0
    mealy_mass = dict()
    mealy_mass[NAME_NEW_POINTS] = []
    for k, point in enumerate(points):
        mealy_mass[NAME_NEW_POINTS].append(point)
    for i, ch in enumerate(input_characters):
        if ch != "":
            mealy_mass[ch] = []

        for k, point in enumerate(points):
            mealy_mass[ch].append(point)
        line_number += 1


    return mealy_mass

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
    return mass

def get_input_characters(moore_mass):
    mass = []
    for key in moore_mass:
        if key_is_system_ch(key): continue
        mass.append(key)
    return mass


def add_points(moore_mass):
    finded_points = 1
    points = []
    stolb = 1
    moore_mass[NAME_NEW_POINTS] = []
    leng = len(moore_mass[NAME_POINTS])
    for i in range(0,  leng-1):
        find_new_point = False
        for k, key in enumerate(moore_mass):
            if k in range(0,2): continue
            if key == NAME_NEW_POINTS: continue
            f1 = moore_mass[key][i]
            f2 = moore_mass[key][i + 1]
            if f1 != f2:
                find_new_point = True
                stolb += 1
                break
        new_point = NAME_NEW_POINTS + str(finded_points)
        moore_mass[NAME_NEW_POINTS].append(new_point)
        if new_point not in points: points.append(new_point)
        if  find_new_point: finded_points += 1
    moore_mass[NAME_NEW_POINTS].append(NAME_NEW_POINTS + str(finded_points))
    points.append(NAME_NEW_POINTS + str(finded_points))
    return points

def key_is_system_ch(key):
    if key in [NAME_NEW_POINTS, NAME_OUTPUT_CH, NAME_POINTS]: return True
    else: return False