import csv
import sys
class linux_sheets():
    file_name = sys.argv[1]
    with open(file_name, 'r') as file:
        contents = csv.reader(file, delimiter=',')
        for row in contents:
            print "|",
            for index in range(len(row)):
                print row[index]+" |",
            print ""
