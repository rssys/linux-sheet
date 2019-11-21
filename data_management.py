import csv
import sys
import curses
import settings

def save_data():
    with open('test_file_2.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(settings.contents)

def read_CSV(stdscr, file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        # get as 2d list, but sum() flattens it into 1d list
        contents = list(reader)
    return contents
