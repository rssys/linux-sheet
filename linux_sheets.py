import csv
import sys
class linux_sheets():
    file_name = sys.argv[1]
    with open(file_name, 'r') as file:
        contents = [line.split() for line in file]
        print contents
