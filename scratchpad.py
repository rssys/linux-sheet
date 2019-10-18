import csv
import sys
import curses

contents = []


def main(stdscr):
    file_name = sys.argv[1]
    global contents
    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        # get as 2d list, but sum() flattens it into 1d list
        contents = list(reader)

    h, w = stdscr.getmaxyx()
    stdscr.refresh()
    stdscr.move(0,0)
    contents.append(['0|0|splendid'])
    print int("['4")
    for row in contents:
        for element in row:
            print element

    while True:
        key = stdscr.getch()


if __name__ == '__main__':
    curses.wrapper(main)
