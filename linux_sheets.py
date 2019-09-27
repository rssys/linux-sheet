import csv
import sys
import curses

def createGrid(stdscr, data, max_row_len, current_row_idx, current_col_idx):
    h, w = stdscr.getmaxyx()

    # cell width and height let us do formatted printing and navigate through each cell
    cell_h = 3
    cell_w = 10
    # offsets for when user scrolls down
    h_offset = 0
    w_offset = 0

    if current_row_idx * cell_h > h:
        h_offset = current_row_idx * cell_h - h
    if current_col_idx * cell_w > w:
        w_offset = current_col_idx * cell_w - w
    # create the grid
    grid = curses.newpad(h + h_offset, w + w_offset)
    # loop through array
    for row_idx, row in enumerate(data):
        y = (row_idx * cell_h) + 1
        bot_line_y = y+1
        grid.hline(bot_line_y,0,'-',w)
        for col_idx in range(max_row_len):
            x = col_idx * cell_w
            right_line_x = x+10
            grid.vline(0,right_line_x,'-',h)
            if col_idx < len(data[row_idx]):
                grid.addstr(y,x, data[row_idx][col_idx])
    print("current", h_offset,"height = ",h)
    # refresh pad depending on where user is and move cursor
    if current_row_idx * cell_h > h:
        if current_col_idx * cell_w > w:
            grid.refresh(h_offset,w_offset,0,0,h,w)
            stdscr.move((current_row_idx * cell_h) - (h_offset) + 1, (current_col_idx * cell_w) - w_offset)
        else:
            grid.refresh(h_offset,0,0,0,h,w)
            stdscr.move((current_row_idx * cell_h) - (h_offset)-3 + 1, (current_col_idx * cell_w))
    else:
        if current_col_idx * cell_w > w:
            grid.refresh(0,w_offset,0,0,h,w)
            stdscr.move((current_row_idx * cell_h), (current_col_idx * cell_w) - w_offset)
        else:
            grid.refresh(0,0,0,0,h,w)
            stdscr.move((current_row_idx * cell_h), (current_col_idx * cell_w))
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
        elif key == curses.KEY_DOWN: #elif key == curses.KEY_DOWN and current_row_idx < len(contents) - 1:
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
