import sys

from mealy import mealy_transform_to_min

COMMAND_MEALY = "mealy"
COMMAND_MOORE = "moore"


# program moore-to-mealy moore.csv mealy.csv
# program mealy-to-moore mealy.csv moore.csv
def main(args):
    command = COMMAND_MEALY #args[0]
    input_file_name = "1mea.csv" #args[1]
    output_file_name = "mealy_min.csv" #args[2]
    input_file = open(input_file_name, "r")
    output_file = open(output_file_name, "w")
    mealy_transform_to_min(input_file, output_file)


if __name__ == '__main__':
    main(sys.argv[1:])