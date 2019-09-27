import csv
import sys
import curses

def createGrid(stdscr, data, max_row_len, current_row_idx, current_col_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    # cell width and height let us do formatted printing and navigate through each cell
    cell_h = (h//len(data))
    cell_w = (w//max_row_len)
    for row_idx, row in enumerate(data):
        y = row_idx * cell_h
        for col_idx in range(max_row_len):
            x = col_idx * cell_w
            if col_idx < len(data[row_idx]):
                stdscr.addstr(y,x, data[row_idx][col_idx])
    stdscr.move(current_row_idx * cell_h, current_col_idx * cell_w)
    stdscr.refresh()

def main(stdscr):
    file_name = sys.argv[1]
    contents = []
    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        contents = list(reader)
    # stdscr = curses.initscr()
    print contents
    max_row_len = len(max(contents,key=len))

    # keep track of where user is
    current_row_idx = 0
    current_col_idx = 0

    # initial drawing of grid
    stdscr.move(0,0)
    stdscr.refresh()
    createGrid(stdscr, contents, max_row_len, current_row_idx, current_col_idx)


    while 1:
        # read in user input
        key = stdscr.getch()
        # user navigation
        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -=1
        elif key == curses.KEY_DOWN and current_row_idx < len(contents) - 1:
            current_row_idx += 1
        elif key == curses.KEY_LEFT and current_col_idx > 0:
            current_col_idx -= 1
        elif key == curses.KEY_RIGHT and current_col_idx < (max_row_len - 1):
            current_col_idx += 1

        createGrid(stdscr, contents, max_row_len, current_row_idx, current_col_idx)
    # # terminates a curses program
    # curses.nocbreak()
    # stdscr.keypad(False)
    # curses.echo()
    # # restores terminal to original mode
    # curses.endwin()

if __name__ == '__main__':
    curses.wrapper(main)
