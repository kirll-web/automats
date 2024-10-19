import sys
import mealyToMoor
import moorToMealy

COMMAND_MEALY_TO_MOORE = "mealy-to-moore"
COMMAND_MOORE_TO_MEALY = "moore-to-mealy"


# program moore-to-mealy moore.csv mealy.csv
# program mealy-to-moore mealy.csv moore.csv
def main(args):
    command = COMMAND_MOORE_TO_MEALY# args[0]
    input_file_name =  "6moo.csv"# args[1]
    output_file_name = "6mea.csv" #args[2]
    input_file = open(input_file_name, "r")
    output_file = open(output_file_name, "w")
    if command == COMMAND_MEALY_TO_MOORE:
        mealyToMoor.mealy_to_moore(input_file, output_file)

    if command == COMMAND_MOORE_TO_MEALY:
        moorToMealy.moore_to_mealy(input_file, output_file)


if __name__ == '__main__':
    main(sys.argv[1:])
