import sys

from mealy import mealy_transform_to_min
from moore import moore_transform_to_min

COMMAND_MEALY = "mealy"
COMMAND_MOORE = "moore"


# program moore-to-mealy moore.csv mealy.csv
# program mealy-to-moore mealy.csv moore.csv
def main(args):
    input_file = open(args[1], "r")
    output_file = open(args[2], "w+")
    if args[0] == COMMAND_MEALY:
        mealy_transform_to_min(input_file, output_file)
    if args[0] == COMMAND_MOORE:
        moore_transform_to_min(input_file, output_file)


if __name__ == '__main__':
    main(sys.argv[1:])