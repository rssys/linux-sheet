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
    # test appending to the list
    while len(contents) < 4:
        contents.append([])
    contents[3].append([',,splendid'])

    # pad contents with commas
    max_len = max(len(x) for x in contents)
    print(max_len)
    for index, element in enumerate(contents):
        x =len(element)
        for y in range(x, max_len):
            contents[index].append('')
            # print(y, max_len)
    # print int("['4")
    print(contents)
    # for row in contents:
    #     for element in row:
    #         print element
    stdscr.refresh()
    with open('test_file_3.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(contents)
    while True:
        key = stdscr.getch()


if __name__ == '__main__':
    curses.wrapper(main)
