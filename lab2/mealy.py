NAME_POINTS = "Q"
NUMBER_POINTS = 1
SEPARATOR = ";"

def mealy_transform_to_min(input_file, output_file):
    lines = input_file.readlines()
    mealy_mass = get_mealy_mass(lines)



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