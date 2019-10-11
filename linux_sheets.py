import csv
import sys
import curses

# global variables
user_exited = False
# cell width and height let us do formatted printing and navigate through each cell
cell_h = 2
cell_w = 12
# gap at top and left of screen for the bar
top_margin = 3
bottom_margin = 1
left_margin = 3
# constant to make sure we jump to the start of the word and not the edge of a cell
dist_from_wall = 1

def navigate_help_menu():
    pass


def pop_up_help(stdscr):
    h, w = stdscr.getmaxyx()
    # manual = curses.newpad(h, w)
    manual = curses.newwin(h, w)
    manual.box()
    manual.addstr(1,1,"this is the help menu")
    manual.addstr(2,1,"Navigation: Arrow keys")
    manual.addstr(3,1,"To input data: 'i', enter data")
    manual.addstr(3,1,"To input data: 'i', enter data")
    # manual.refresh(0,0,0,0,h,w)
    manual.refresh()
    exit_menu = False
    manual_y = 0
    manual_x = 0
    while exit_menu == False:
        key = stdscr.getch()
        navigating = False
        if key == curses.KEY_UP and manual_y > 0:
            manual_y -=1
            navigating = True
        elif key == curses.KEY_DOWN:
            manual_y += 1
            navigating = True
        elif key == curses.KEY_LEFT and manual_x > 0:
            manual_x -= 1
            navigating = True
        elif key == curses.KEY_RIGHT:
            manual_x += 1
            navigating = True
        if navigating == True:
            navigate_help_menu()
        elif key == 27:
            exit_menu = True
    stdscr.clear()


def big_commands(stdscr):
    h, w = stdscr.getmaxyx()
    curses.echo()
    stdscr.addstr(h-1,0,":")
    command = stdscr.getstr(h-1,1)
    curses.noecho()
    if command == "wq":
        global user_exited
        user_exited = True

def write_to_cell(stdscr, current_row_idx, current_col_idx):
    curses.echo()
    stdscr.getstr(current_row_idx * cell_h + top_margin, current_col_idx * cell_w + dist_from_wall)
    curses.noecho()

def createGrid(stdscr, data, current_row_idx, current_col_idx):
    h, w = stdscr.getmaxyx()

    # height and width of the grid window
    grid_h = h - top_margin - bottom_margin
    grid_w = w - left_margin
    # offsets for when user scrolls down
    h_offset = 0
    w_offset = 0

    # set offsets
    if current_row_idx * cell_h >= grid_h:
        h_offset = current_row_idx * cell_h - grid_h
        h_offset += (cell_h - h_offset % cell_h)
    if current_col_idx * cell_w + dist_from_wall >= grid_w:
        w_offset = current_col_idx * cell_w + dist_from_wall - grid_w
        # print w_offset
        w_offset += (cell_w - w_offset % cell_w)
        # print w_offset

    # create the grid
    grid = curses.newpad(grid_h + h_offset, grid_w + w_offset)

    # loop through array
    # print data
    for element in data:
        element_parts = str(element).split('|')
        y = int(element_parts[0]) * cell_h
        x = int(element_parts[1]) * cell_w
        element_str = element_parts[2]
        if y < grid_h + h_offset and x+dist_from_wall < w+w_offset: #if y + top_margin < grid_h + h_offset and x+dist_from_wall+left_margin < w+w_offset:
            grid.addstr(y,x+dist_from_wall, element_str)

    # draw the horizontal lines
    for h_line in range(1,(grid_h+h_offset)//cell_h + 1):
        y = (h_line * cell_h) - 1
        grid.hline(y,0,'-',grid_w+w_offset)
    # draw the vertical lines
    for v_line in range(0,(grid_w+w_offset)//cell_w + 1):
        x = (v_line * cell_w)
        if x < grid_w+w_offset:
            grid.vline(0,x,'|',grid_h+h_offset)

    # refresh pad depending on where user is and move cursor
    grid.move((current_row_idx * cell_h), dist_from_wall+(current_col_idx * cell_w))
    # variables for changing what portions of the screen to display
    display_h = 0
    display_w = 0
    # get display height
    if current_row_idx * cell_h > grid_h:
        # print(h_offset)
        # if grid_h % cell_h == 0:
        #     display_h = cell_h + h_offset
            # grid.refresh(cell_h+h_offset,0,top_margin,0,grid_h,w)
        # else:
        display_h = h_offset
            # grid.refresh(h_offset,0,top_margin,0,grid_h,w)
    else:
        # print(current_row_idx*cell_h)
        if current_row_idx * cell_h == grid_h:
            display_h = cell_h
            # grid.refresh(cell_h,0,top_margin,0,grid_h,w)
        else:
            display_h = 0
            # grid.refresh(0,0,top_margin,0,grid_h,w)

    # get display width
    if current_col_idx * cell_w + dist_from_wall > grid_w:
        # if grid_w % cell_w == 0:
        display_w = w_offset
            # grid.refresh(cell_h+h_offset,0,top_margin,0,grid_h,w)
            # print display_w
        # else:
            # display_w = w_offset
            # print current_col_idx * cell_w + dist_from_wall
        # display_w = w_offset
        # print w_offset
    else:
        # # print(current_row_idx*cell_h)
        if current_col_idx * cell_w + dist_from_wall == grid_w:
            display_w = cell_w
            # grid.refresh(cell_h,0,top_margin,0,grid_h,w)
        else:
            display_w = 0
            # print current_col_idx * cell_w + dist_from_wall

    grid.refresh(display_h,display_w,top_margin,left_margin,h-bottom_margin,w)

def main(stdscr):
    file_name = sys.argv[1]
    contents = []
    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        # get as 2d list, but sum() flattens it into 1d list
        contents = sum(list(reader),[])
    # stdscr = curses.initscr()

    # keep track of where user is
    current_row_idx = 0
    current_col_idx = 0

    # initial drawing of grid
    stdscr.refresh()
    createGrid(stdscr, contents, current_row_idx, current_col_idx)


    while user_exited == False:
        # read in user input
        key = stdscr.getch()
        # user navigation
        navigating = False
        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -=1
            navigating = True
        elif key == curses.KEY_DOWN:
            current_row_idx += 1
            navigating = True
        elif key == curses.KEY_LEFT and current_col_idx > 0:
            current_col_idx -= 1
            navigating = True
        elif key == curses.KEY_RIGHT:
            current_col_idx += 1
            navigating = True
        elif key == ord('h'):
            pop_up_help(stdscr)
        elif key == ord('i'):
            write_to_cell(stdscr, current_row_idx, current_col_idx)
        elif key == ord(':'):
            big_commands(stdscr)
            print user_exited
        if navigating is True:
            createGrid(stdscr, contents, current_row_idx, current_col_idx)

if __name__ == '__main__':
    curses.wrapper(main)
