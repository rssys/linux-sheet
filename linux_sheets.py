import csv
import sys
import curses

def createGrid(stdscr, data):
    max_row_len = len(max(data,key=len))
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for row_idx, row in enumerate(data):
        y = row_idx * (h//len(data))
        for col_idx in range(max_row_len):
            x = col_idx * (w//max_row_len)
            if col_idx < len(data[row_idx]):
                stdscr.addstr(y,x, data[row_idx][col_idx])
    stdscr.refresh()

def main(stdscr):
    file_name = sys.argv[1]
    contents = []
    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        contents = list(reader)
    # stdscr = curses.initscr()
    print contents
    createGrid(stdscr, contents)

    while 1:
        key = stdscr.getch()

        stdscr.clear()

        if key == curses.KEY_UP:
            stdscr.addstr(0,0,"you pressed up!")
        elif key == curses.KEY_DOWN:
            stdscr.addstr(0,0,"you pressed down!")
        stdscr.refresh()

    # # terminates a curses program
    # curses.nocbreak()
    # stdscr.keypad(False)
    # curses.echo()
    # # restores terminal to original mode
    # curses.endwin()

if __name__ == '__main__':
    curses.wrapper(main)
