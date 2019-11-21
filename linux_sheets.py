import csv
import sys
import curses
import settings

from data_management import read_CSV
from data_management import save_data
from data_management import write_to_cell
from grid_creation import create_without_grid_lines
from grid_creation import create_with_grid_lines
from dimensions import get_dimensions
from help_menu import navigate_help_menu
from help_menu import pop_up_help

# def get_csv_string_format(user_input, row, col):
#     return str(row) + "|" + str(col) + "|" + user_input

def index_contents(stdscr):
    for index, element in enumerate(settings.contents):
        element_parts = str(element).split('|')
        y = element_parts[0][2:] #we have to take from the second index because for some reason each element has the bracket and single quotes included
        x = element_parts[1]
        # stdscr.move(0,0)
        # stdscr.addstr(str(y))
        # break
        settings.index_dict[y + x] = index

def navigate_help_menu():
    pass

def big_commands(stdscr):
    h, w = stdscr.getmaxyx()
    curses.echo()
    stdscr.addstr(h-1,0,":")
    command = stdscr.getstr(h-1,1)
    curses.noecho()
    if command == "wq":
        settings.user_exited = True
        save_data()

# def write_to_cell(stdscr):
#     curses.echo()
#     # user_input = stdscr.getstr(current_row_idx + top_margin - h_holder, current_col_idx * cell_w + dist_from_wall + left_margin - w_holder)
#     h, w = stdscr.getmaxyx()
#     user_input = stdscr.getstr(h-1, 0)
#     curses.noecho()
#     if (str(settings.current_row_idx) + str(settings.current_col_idx)) in settings.index_dict:
#         settings.contents[settings.index_dict[str(settings.current_row_idx) + str(settings.current_col_idx)]] = [get_csv_string_format(user_input, settings.current_row_idx, settings.current_col_idx)]
#     else:
#         settings.index_dict[str(settings.current_row_idx) + str(settings.current_col_idx)] = len(settings.contents)
#         settings.contents.append([get_csv_string_format(user_input, settings.current_row_idx, settings.current_col_idx)])
#     #TODO update the data
#     stdscr.move(settings.current_row_idx + settings.top_margin - settings.h_holder, settings.current_col_idx * settings.cell_w + settings.dist_from_wall + settings.left_margin - settings.w_holder)
#     # repaint the grid so the previous word is not still on screen
#     create_without_grid_lines(stdscr)
#     # print index_dict

def main(stdscr):
    file_name = sys.argv[1]
    settings.contents = read_CSV(stdscr, file_name)
    index_contents(stdscr)

    # create color schemes for the top and bottom margins
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # # initial drawing of grid
    create_without_grid_lines(stdscr)

    while settings.user_exited == False:
        # read in user input
        key = stdscr.getch()
        # get dimensions to check for scrolling
        grid_h, grid_w = get_dimensions(stdscr)
        # user navigation
        navigating = False
        if key == curses.KEY_UP and settings.current_row_idx > 0:
            settings.current_row_idx -= 1
            if settings.current_row_idx < settings.h_holder:
                settings.h_holder -= 1
            navigating = True
        elif key == curses.KEY_DOWN:
            settings.current_row_idx += 1
            if settings.current_row_idx >= settings.h_holder + grid_h:
                settings.h_holder += 1
            navigating = True
        elif key == curses.KEY_LEFT and settings.current_col_idx > 0:
            settings.current_col_idx -= 1
            if settings.current_col_idx * settings.cell_w +settings.dist_from_wall <= settings.w_holder:
                settings.w_holder -= settings.cell_w
            navigating = True
        elif key == curses.KEY_RIGHT:
            settings.current_col_idx += 1
            if settings.current_col_idx * settings.cell_w + settings.dist_from_wall >= settings.w_holder + grid_w:
                settings.w_holder += settings.cell_w
            navigating = True
        elif key == ord('h'):
            pop_up_help(stdscr)
        elif key == ord('i'):
            write_to_cell(stdscr)
            # repaint the grid to update the new word written to the screen
            create_without_grid_lines(stdscr)
        elif key == ord(':'):
            big_commands(stdscr)
            # print user_exited
        if navigating is True or key == curses.KEY_RESIZE:
            # move the user cursor to the top left corner so if the window gets small, the cursor won't go offscreen
            if key == curses.KEY_RESIZE:
                settings.current_row_idx = settings.h_holder
                settings.current_col_idx = settings.w_holder//settings.cell_w
                stdscr.move(0, 0)
            # create_with_grid_lines(stdscr)
            create_without_grid_lines(stdscr)

if __name__ == '__main__':
    curses.wrapper(main)
