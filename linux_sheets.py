import csv
import sys
import curses

def pop_up_help(stdscr):
    h, w = stdscr.getmaxyx()
    manual = curses.newwin(5,50, h//2, w//2)
    manual.box()
    manual.addstr("this is the help menu", )
    manual.refresh()

# def write_to_cell(current_row_idx, current_col_idx):


def createGrid(stdscr, data, max_row_len, current_row_idx, current_col_idx):
    h, w = stdscr.getmaxyx()

    # cell width and height let us do formatted printing and navigate through each cell
    cell_h = 2
    cell_w = 12

    # offsets for when user scrolls down
    h_offset = 0
    w_offset = 0

    # gap at top of screen for the bar
    top_bar_h = 1

    # height of the grid window
    grid_h = h - top_bar_h

    # constant to make sure we jump to the start of the word and not the edge of a cell
    dist_from_wall = 1

    # set offsets
    if current_row_idx * cell_h > grid_h:
        h_offset = current_row_idx * cell_h - grid_h
        h_offset += h_offset % cell_h
    if current_col_idx * cell_w > w:
        w_offset = current_col_idx * cell_w - w
        w_offset += w_offset % cell_w

    # create the grid
    grid = curses.newpad(h + h_offset, w + w_offset)

    # loop through array
    # print data
    for element in data:
        element_parts = str(element).split('|')
        y = int(element_parts[0]) * cell_h
        x = int(element_parts[1]) * cell_w
        element_str = element_parts[2]
        if y < grid_h + h_offset and x+dist_from_wall < w+w_offset:
            grid.addstr(y,x+dist_from_wall, element_str)

    # # loop through array
    # for row_idx, row in enumerate(data):
    #     y = (row_idx * cell_h)
    #     for col_idx in range(max_row_len):
    #         x = col_idx * cell_w
    #         if col_idx < len(data[row_idx]):
    #             if y < h + h_offset and x+dist_from_wall < w+w_offset:
    #                 grid.addstr(y,x+dist_from_wall, data[row_idx][col_idx])

    # draw the horizontal lines
    for h_line in range((h+h_offset)//cell_h):
        y = (h_line * cell_h) + 1
        grid.hline(y,0,'-',w+w_offset)
    # draw the vertical lines
    for v_line in range(1,(w+w_offset)//cell_w):
        x = (v_line * cell_w)
        grid.vline(0,x,'|',h+h_offset)

    # print("current",current_row_idx * cell_h,"height = ",h+h_offset)
    # refresh pad depending on where user is and move cursor
    if current_row_idx * cell_h > grid_h:
        # print(h_offset)
        grid.move((current_row_idx * cell_h), dist_from_wall+(current_col_idx * cell_w))
        if grid_h % cell_h == 0:
            grid.refresh(cell_h+h_offset,0,top_bar_h,0,grid_h,w)
        else:
            grid.refresh(h_offset,0,top_bar_h,0,grid_h,w)
    else:
        # print(current_row_idx*cell_h)
        grid.move((current_row_idx * cell_h), dist_from_wall+(current_col_idx * cell_w))
        if current_row_idx*cell_h == grid_h:
            grid.refresh(cell_h,0,top_bar_h,0,grid_h,w)
        else:
            grid.refresh(0,0,top_bar_h,0,grid_h,w)


def main(stdscr):
    file_name = sys.argv[1]
    contents = []
    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        # get as 2d list, but sum() flattens it into 1d list
        contents = sum(list(reader),[])
    # stdscr = curses.initscr()
    max_row_len = len(max(contents,key=len))

    # keep track of where user is
    current_row_idx = 0
    current_col_idx = 0

    # initial drawing of grid
    stdscr.refresh()
    createGrid(stdscr, contents, max_row_len, current_row_idx, current_col_idx)


    while 1:
        # read in user input
        key = stdscr.getch()
        # user navigation
        navigating = False
        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -=1
            navigating = True
        elif key == curses.KEY_DOWN: #elif key == curses.KEY_DOWN and current_row_idx < len(contents) - 1:
            current_row_idx += 1
            navigating = True
        elif key == curses.KEY_LEFT and current_col_idx > 0:
            current_col_idx -= 1
            navigating = True
        elif key == curses.KEY_RIGHT: #and current_col_idx < (max_row_len - 1)
            current_col_idx += 1
            navigating = True
        elif key == ord('f'):
            pop_up_help(stdscr)
        # elif key == '\n' or key == 13:

        if navigating is True:
            createGrid(stdscr, contents, max_row_len, current_row_idx, current_col_idx)
    # # terminates a curses program
    # curses.nocbreak()
    # stdscr.keypad(False)
    # curses.echo()
    # # restores terminal to original mode
    # curses.endwin()

if __name__ == '__main__':
    curses.wrapper(main)
