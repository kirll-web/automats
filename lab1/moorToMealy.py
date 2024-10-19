import bisect
def moore_to_mealy(input_file, output_file):
    lines = input_file.readlines()

    moore_mass = get_moore_mass(lines)
    points = add_points(moore_mass)
    input_characters = get_input_characters(moore_mass)
    mealy_mass = create_mealy(input_characters, points)


    last_item = ""
    for i, item in enumerate(moore_mass[len(moore_mass) - 1]):
        if last_item == item: continue
        last_item = item
        for k in range(2, len(moore_mass)-1) :
            old_point = moore_mass[k][i]
            moor_input_ch = moore_mass[k][0]

            mealy_index_input_ch = 0
            for b in range(1,len(moore_mass)-1):
                if mealy_mass[b][0] == moor_input_ch:
                    mealy_index_input_ch = b
                    break

            new_moore_point = moore_mass[len(moore_mass)-1][moore_mass[1].index(old_point)]

            mealy_index_point = bisect.bisect_left(mealy_mass[0], item)

            moore_output_ch = moore_mass[0][bisect.bisect_left(moore_mass[1], old_point)]

            mealy_mass[mealy_index_input_ch][mealy_index_point] = new_moore_point + "/" + moore_output_ch

    for i, line in enumerate(mealy_mass):
        for k, ch in enumerate(line):
            output_file.write(ch)
            if k < len(line) - 1: output_file.write(";")
        output_file.write("\n")
    for i, line in enumerate(mealy_mass):
        print(line)



    return 5
#TODO создание автомата мили:
# можно модифицировать moore_mass
# снизу/сверху каждой вершины добавить её новый номер
# читаем также как и при получении вершин и держим в памяти какая вершина была предыдушей
# если она равна предыдущей, то пропускаем данный столбик

def create_mealy(input_characters, points):
    line_number = 0
    mealy_mass = []
    mealy_mass.append([""])
    for i, ch in enumerate(input_characters):
        if ch != "":
            mealy_mass.append([ch])

        for k, point in enumerate(points):
            mealy_mass[line_number].append(point)
        line_number += 1
    for k, point in enumerate(points):
        mealy_mass[line_number].append(point)

    return mealy_mass

def get_moore_mass(lines):
    mass = [[] for _ in range(len(lines))]
    for i, line in enumerate(lines):
        temp = line.strip().split(";")
        mass[i] = temp
    return mass

def get_input_characters(moore_mass):
    mass = []
    for i in range(1, len(moore_mass)):
        if moore_mass[i][0] != "": mass.append(moore_mass[i][0])
    return mass


def add_points(moore_mass):
    points = []
    finded_points = 1
    points = []
    line = 2
    stolb = 1
    moore_mass.append([""])
    new_point = ""
    for i in range(1, len(moore_mass[0])-1):
        find_new_point = False
        for k in range(line, len(moore_mass) - 1):
            f1 = moore_mass[k][i]
            f2 = moore_mass[k][i + 1]
            if f1 != f2:
                find_new_point = True
                stolb += 1
                break
        new_point = "F" + str(finded_points)
        moore_mass[len(moore_mass) - 1].append(new_point)
        if new_point not in points: points.append(new_point)
        if  find_new_point: finded_points += 1
    moore_mass[len(moore_mass) - 1].append("F" + str(finded_points))
    points.append("F" + str(finded_points))
    return points