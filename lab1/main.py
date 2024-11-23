
import sys
import mealyToMoor
import moorToMealy

COMMAND_MEALY_TO_MOORE = "mealy-to-moore"
COMMAND_MOORE_TO_MEALY = "moore-to-mealy"

# program moore-to-mealy moore.csv mealy.csv
# program mealy-to-moore mealy.csv moore.csv

def main(args):
    #command = args[0]
    #command = COMMAND_MEALY_TO_MOORE  # args[0]
    command = args[0]
    input_file_name = args[1]
    output_file_name = args[2]
    #input_file_name = "6mea.csv" #moore to mealy
    #output_file_name = "X:\\automatsLabs\\lab1\\CREATED.csv"  #moore to mealy
    #input_file_name = "4mea.csv"  # mealy to moore
    #output_file_name = "4moo.csv"  # mealy to moore
    input_file = open(input_file_name, "r")
    output_file = open(output_file_name, "w+")
    output_file.write("я ТТУУУУ")
    if command == COMMAND_MEALY_TO_MOORE:
        mealyToMoor.mealy_to_moore(input_file, output_file)

    if command == COMMAND_MOORE_TO_MEALY:
        moorToMealy.moore_to_mealy(input_file, output_file)
    output_file.close()

if __name__ == '__main__':
    main(sys.argv[1:])
