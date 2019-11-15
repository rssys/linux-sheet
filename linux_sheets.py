import csv
import sys
import curses

# global variables
# the contents of the csv file
contents = []
index_dict = {}
# placeholder variables for the top left corner so we can know when to scroll
h_holder = 0
w_holder = 0
# keep track of where user is
current_row_idx = 0
current_col_idx = 0
# boolean to keep track of when to exit the program
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
# to keep track of where the screen is to determine if scrolling is needed
current_display_h = 0
current_display_w = 0

def get_csv_string_format(user_input, row, col):
    return str(row) + "|" + str(col) + "|" + user_input

def index_contents(stdscr):
    global index_dict
    for index, element in enumerate(contents):
        element_parts = str(element).split('|')
        y = element_parts[0][2:] #we have to take from the second index because for some reason each element has the bracket and single quotes included
        x = element_parts[1]
        # stdscr.move(0,0)
        # stdscr.addstr(str(y))
        # break
        index_dict[y + x] = index

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
        elif key == 27: #escape key
            exit_menu = True
    create_without_grid_lines(stdscr)

def save_data():
    with open('test_file_2.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(contents)

def big_commands(stdscr):
    h, w = stdscr.getmaxyx()
    curses.echo()
    stdscr.addstr(h-1,0,":")
    command = stdscr.getstr(h-1,1)
    curses.noecho()
    if command == "wq":
        global user_exited
        user_exited = True
        save_data()

def write_to_cell(stdscr):
    global current_row_idx
    global current_col_idx
    curses.echo()
    # user_input = stdscr.getstr(current_row_idx + top_margin - h_holder, current_col_idx * cell_w + dist_from_wall + left_margin - w_holder)
    h, w = stdscr.getmaxyx()
    user_input = stdscr.getstr(h-1, 0)
    curses.noecho()
    if (str(current_row_idx) + str(current_col_idx)) in index_dict:
        contents[index_dict[str(current_row_idx) + str(current_col_idx)]] = [get_csv_string_format(user_input, current_row_idx, current_col_idx)]
    else:
        index_dict[str(current_row_idx) + str(current_col_idx)] = len(contents)
        contents.append([get_csv_string_format(user_input, current_row_idx, current_col_idx)])
    #TODO update the data
    stdscr.move(current_row_idx + top_margin - h_holder, current_col_idx * cell_w + dist_from_wall + left_margin - w_holder)
    # repaint the grid so the previous word is not still on screen
    create_without_grid_lines(stdscr)
    # print index_dict

def get_col_string(num):
    string = ""
    while num > 0:
        num, remainder = divmod(num - 1, 26)
        string = chr(65 + remainder) + string
    return string

def print_row_numbers(stdscr, grid_h):
    # print row numbers and column letters on top and left margins
    # stdscr.attron(curses.color_pair(1))
    for a in range(grid_h):
        # stdscr.addstr(top_margin + a, 0, str(a + h_holder + 1)) #add the plus one becuase we start at 1
        stdscr.addstr(top_margin + a, 0, str(a + h_holder + 1).rjust(left_margin)) #add the plus one becuase we start at 1
    # stdscr.attroff(curses.color_pair(1))


def print_col_letters(stdscr, grid_w, cell_w):
    # stdscr.attron(curses.color_pair(1))
    for a in range(grid_w//cell_w): #TODO this writes to parts that are partially shown but in the case where the string is the bottom right corner it messes up
    # for a in range(grid_w//cell_w + 1): this sometimes works but if you resize it a certain way it prints the last col unumber on the next row
        a_str = get_col_string(w_holder//cell_w + a + 1) #we send in 0 on the first call but need to start at 1
        stdscr.addstr(2, left_margin + (a*cell_w), a_str.center(cell_w))
        # stdscr.addstr(2, left_margin + (cell_w//2)+(a*cell_w), a_str)
    # stdscr.attroff(curses.color_pair(1))

def create_with_grid_lines(stdscr):
    global current_row_idx
    global current_col_idx
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
    for row in contents:
        for element in row:
            element_parts = str(element).split('|')
            y = int(element_parts[0]) * cell_h
            x = int(element_parts[1]) * cell_w
            element_str = element_parts[2]
            if y < grid_h + h_offset and x+dist_from_wall < grid_w+w_offset:
            # if y + top_margin < grid_h + h_offset and x+dist_from_wall+left_margin < w+w_offset:
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
        display_h = h_offset
    else:
        if current_row_idx * cell_h == grid_h:
            display_h = cell_h
        else:
            display_h = 0

    # get display width
    if current_col_idx * cell_w + dist_from_wall > grid_w:
        display_w = w_offset
    else:
        if current_col_idx * cell_w + dist_from_wall == grid_w:
            display_w = cell_w
        else:
            display_w = 0

    grid.refresh(display_h,display_w,top_margin,left_margin,h-bottom_margin,w)

def get_dimensions(stdscr):
    h, w = stdscr.getmaxyx()

    # height and width of the grid window
    grid_h = h - top_margin - bottom_margin
    grid_w = w - left_margin
    return grid_h, grid_w

def print_data(grid, grid_h, grid_w):
    # print data
    for row in contents:
        for element in row:
            element_parts = str(element).split('|')
            y = int(element_parts[0])
            x = int(element_parts[1]) * cell_w
            element_str = element_parts[2]

            if y < h_holder + grid_h and y >= h_holder:
                if x + dist_from_wall < w_holder + grid_w  and x + dist_from_wall >= w_holder:
                # TODO if x + dist_from_wall < w_holder + grid_w - cell_w and x + dist_from_wall >= w_holder: this will write the strings but it could result in the bottom right corner
                # being written to which causes an error so find a way around that
                    # grid.addstr(y,x + dist_from_wall, str(y)+" "+str(x)+" "+str(h_holder)+" "+str(w_holder))
                    # try:
                    #     grid.addstr(y,x + dist_from_wall, str(y)+" "+str(x)+" "+str(h_holder)+" "+str(w_holder))
                    # except(curses.error):
                    #     print (grid_h+h_holder, grid_h+h_offset)
                    # check if we need to truncate the right most column strings
                    if w_holder + grid_w - (x + dist_from_wall) < cell_w:
                        grid.addstr(y,x + dist_from_wall, element_str[:(w_holder + grid_w - (x + dist_from_wall)-1 )]) #subtract 1 because we can't write to the bottom right corner of the screen
                    else:
                        grid.addstr(y,x + dist_from_wall, element_str[:cell_w])

def print_current_location(stdscr):
    # stdscr.addstr(0, 0, 'row: ' + str(current_row_idx) + ' col: ' + str(current_col_idx))
    stdscr.addstr(0, 0, 'row: ' + str(current_row_idx) + ' col: ' + str(current_col_idx) + ' h_holder: '+str(h_holder) + ' w_holder: '+str(w_holder))

def create_without_grid_lines(stdscr):
    # need to erase to clear any strings that were previously painted that now shouldn't be there
    stdscr.erase()
    global current_row_idx
    global current_col_idx
    global current_display_h
    global current_display_w

    h, w = stdscr.getmaxyx()
    grid_h, grid_w = get_dimensions(stdscr)

    # create the grid
    grid = curses.newpad(grid_h + h_holder, grid_w + w_holder)

    print_current_location(stdscr)
    print_data(grid, grid_h, grid_w)


    print_col_letters(stdscr, grid_w, cell_w)
    print_row_numbers(stdscr, grid_h)
    stdscr.refresh()
    # refresh pad depending on where user is and move cursor
    grid.move((current_row_idx), dist_from_wall+(current_col_idx * cell_w))
    grid.refresh(h_holder,w_holder,top_margin,left_margin,h-bottom_margin,w)

def main(stdscr):
    file_name = sys.argv[1]
    global contents
    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter='\n')
        # get as 2d list, but sum() flattens it into 1d list
        contents = list(reader)
    index_contents(stdscr)

    # keep track of where user is
    global current_row_idx
    global current_col_idx
    # keep track of when we need to scroll
    global h_holder
    global w_holder
    # create color schemes for the top and bottom margins
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # # initial drawing of grid
    # stdscr.refresh()
    # create_with_grid_lines(stdscr)
    create_without_grid_lines(stdscr)


    while user_exited == False:
        # read in user input
        key = stdscr.getch()
        # get dimensions to check for scrolling
        grid_h, grid_w = get_dimensions(stdscr)
        # user navigation
        navigating = False
        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
            if current_row_idx < h_holder:
                h_holder -= 1
            navigating = True
        elif key == curses.KEY_DOWN:
            current_row_idx += 1
            if current_row_idx >= h_holder + grid_h:
                h_holder += 1
            navigating = True
        elif key == curses.KEY_LEFT and current_col_idx > 0:
            current_col_idx -= 1
            if current_col_idx * cell_w +dist_from_wall <= w_holder:
                w_holder -= cell_w
            navigating = True
        elif key == curses.KEY_RIGHT:
            current_col_idx += 1
            if current_col_idx * cell_w + dist_from_wall >= w_holder + grid_w:
                w_holder += cell_w
            navigating = True
        elif key == ord('h'):
            pop_up_help(stdscr)
        elif key == ord('i'):
            write_to_cell(stdscr)
        elif key == ord(':'):
            big_commands(stdscr)
            # print user_exited
        if navigating is True or key == curses.KEY_RESIZE:
            # move the user cursor to the top left corner so if the window gets small, the cursor won't go offscreen
            if key == curses.KEY_RESIZE:
                current_row_idx = h_holder
                current_col_idx = w_holder//cell_w
                stdscr.move(0, 0)
            # create_with_grid_lines(stdscr)
            create_without_grid_lines(stdscr)

if __name__ == '__main__':
    curses.wrapper(main)
