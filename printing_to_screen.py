import csv
import sys
import curses
import settings

def print_current_location():
    # clears line in case previous string was longer than current element
    settings.stdscr.move(0,0)
    settings.stdscr.clrtoeol()
    if settings.format == "my_format":
        if (str(settings.current_row_idx) + str(settings.current_col_idx)) in settings.index_dict:
            coords_and_user_input = str(settings.contents[settings.index_dict[str(settings.current_row_idx) + str(settings.current_col_idx)]])
            parts = coords_and_user_input[2:-2].split('|') #the [2:-2] is to trim the element so it doesn't have the [''] at the front and end
            user_input = parts[2]
            settings.stdscr.addstr(0, 0, 'row: ' + str(settings.current_row_idx) + ' col: ' + str(settings.current_col_idx) + ' | ' + user_input)
        else:
            settings.stdscr.addstr(0, 0, 'row: ' + str(settings.current_row_idx) + ' col: ' + str(settings.current_col_idx))
    else:
        if settings.current_row_idx < len(settings.contents) and settings.current_col_idx < len(settings.contents[0]) and settings.contents[settings.current_row_idx][settings.current_col_idx] is not '':
                settings.stdscr.addstr(0, 0, 'row: ' + str(settings.current_row_idx + 1) + ' col: ' + get_col_string(settings.current_col_idx + 1) + ' | ' + str(settings.contents[settings.current_row_idx][settings.current_col_idx]))
        else:
            settings.stdscr.addstr(0, 0, 'row: ' + str(settings.current_row_idx + 1) + ' col: ' + get_col_string(settings.current_col_idx + 1))

def print_data():
    # print data
    if settings.format == "my_format":
        # TODO instead of looping through all the data, loop through every spot on screen and check if there is an element there
        for row in settings.contents:
            for element in row:
                element_parts = str(element).split('|')
                y = int(element_parts[0])
                x = int(element_parts[1]) * settings.cell_w
                element_str = element_parts[2]

                if y < settings.h_holder + settings.grid_h and y >= settings.h_holder:
                    if x + settings.dist_from_wall < settings.w_holder + settings.grid_w  and x + settings.dist_from_wall >= settings.w_holder:
                    # TODO if x + dist_from_wall < w_holder + grid_w - cell_w and x + dist_from_wall >= w_holder: this will write the strings but it could result in the bottom right corner
                    # being written to which causes an error so find a way around that
                        # grid.addstr(y,x + dist_from_wall, str(y)+" "+str(x)+" "+str(h_holder)+" "+str(w_holder))
                        # try:
                        #     grid.addstr(y,x + dist_from_wall, str(y)+" "+str(x)+" "+str(h_holder)+" "+str(w_holder))
                        # except(curses.error):
                        #     print (grid_h+h_holder, grid_h+h_offset)
                        # check if we need to truncate the right most column strings
                        if settings.w_holder + settings.grid_w - (x + settings.dist_from_wall) < settings.cell_w:
                            settings.grid.addstr(y,x + settings.dist_from_wall, element_str[:(settings.w_holder + settings.grid_w - (x + settings.dist_from_wall)-1 )]) #subtract 1 because we can't write to the bottom right corner of the screen
                        else:
                            settings.grid.addstr(y,x + settings.dist_from_wall, element_str[:settings.cell_w-1]) # the -1 is to give one space between each cell
    else:
        for row in range(settings.h_holder, settings.h_holder + settings.grid_h):
            for col in range(settings.w_holder//settings.cell_w, (settings.w_holder + settings.grid_w)//settings.cell_w):
                col_position = col * settings.cell_w
                if row < len(settings.contents) and col < len(settings.contents[0]):
                    # check if element is within dimension boundaries
                    # if row < settings.grid_total_h and col < settings.grid_total_w:
                    settings.grid.addstr(row, col_position + settings.dist_from_wall, settings.contents[row][col][:settings.cell_w-1]) # the -1 is to give one space between each cell


def get_col_string(num):
    string = ""
    while num > 0:
        num, remainder = divmod(num - 1, 26)
        string = chr(65 + remainder) + string
    return string

def print_col_letters():
    # settings.stdscr.attron(curses.color_pair(1))
    for a in range(settings.grid_w//settings.cell_w): #TODO this writes to parts that are partially shown but in the case where the string is the bottom right corner it messes up
    # for a in range(grid_w//cell_w + 1): this sometimes works but if you resize it a certain way it prints the last col unumber on the next row
        a_str = get_col_string(settings.w_holder//settings.cell_w + a + 1) #we send in 0 on the first call but need to start at 1
        settings.stdscr.addstr(2, settings.left_margin + (a*settings.cell_w), a_str.center(settings.cell_w))
        # settings.stdscr.addstr(2, left_margin + (cell_w//2)+(a*cell_w), a_str)
    # settings.stdscr.attroff(curses.color_pair(1))

def print_row_numbers():
    # print row numbers and column letters on top and left margins
    # settings.stdscr.attron(curses.color_pair(1))
    for a in range(settings.grid_h):
        # settings.stdscr.addstr(top_margin + a, 0, str(a + h_holder + 1)) #add the plus one becuase we start at 1
        settings.stdscr.addstr(settings.top_margin + a, 0, str(a + settings.h_holder + 1).rjust(settings.left_margin)) #add the plus one becuase we start at 1
    # settings.stdscr.attroff(curses.color_pair(1))
