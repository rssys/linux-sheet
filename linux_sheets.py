import csv
import sys
import curses
import settings

from data_management import read_data
from data_management import save_data
from data_management import index_contents
from data_management import write_to_cell
from grid_creation import create_without_grid_lines
from grid_creation import create_with_grid_lines
from grid_creation import refresh_grid
from dimensions import get_dimensions
from help_menu import navigate_help_menu
from help_menu import pop_up_help
from features import quick_scroll
from features import go_to

def big_commands(stdscr):
    h, w = stdscr.getmaxyx()
    curses.echo()
    stdscr.addstr(h-1,0,":")
    command = stdscr.getstr(h-1,1).decode('utf-8')
    curses.noecho()
    if command == "wq":
        settings.user_exited = True
        save_data()
    try:
        row_num = int(command)
        go_to(row_num)
    except ValueError:
        pass

def main(stdscr):
    settings.file_name = sys.argv[1]
    # set the format that the program will use (either normal CSV with commas or my own with coordinates)
    # settings.format = "my_format"
    settings.format = "CSV"
    read_data(stdscr)
    # index_contents(stdscr)

    # create color schemes for the top and bottom margins
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # get dimensions
    settings.h, settings.w = stdscr.getmaxyx()
    settings.grid_h, settings.grid_w = get_dimensions(stdscr)
    # initial drawing of grid
    create_without_grid_lines(stdscr)

    while settings.user_exited == False:
        # read in user input
        key = stdscr.getch()
        # user navigation
        settings.grid_shifting = False
        if key == curses.KEY_UP and settings.current_row_idx > 0:
            settings.current_row_idx -= 1
            if settings.current_row_idx < settings.h_holder:
                settings.h_holder -= 1
                settings.grid_shifting = True
        elif key == curses.KEY_DOWN:
            settings.current_row_idx += 1
            if settings.current_row_idx >= settings.h_holder + settings.grid_h:
                settings.h_holder += 1
                settings.grid_shifting = True
        elif key == curses.KEY_LEFT and settings.current_col_idx > 0:
            settings.current_col_idx -= 1
            if settings.current_col_idx * settings.cell_w + settings.dist_from_wall <= settings.w_holder:
                settings.w_holder -= settings.cell_w
                settings.grid_shifting = True
        elif key == curses.KEY_RIGHT:
            settings.current_col_idx += 1
            if settings.current_col_idx * settings.cell_w + settings.dist_from_wall >= settings.w_holder + settings.grid_w // settings.cell_w * settings.cell_w: # divide and multiply by cell_w to truncate and make grid_w a multiple of cell_w
                settings.w_holder += settings.cell_w
                settings.grid_shifting = True
        elif key == ord('h'):
            pop_up_help(stdscr)
            # repaint the grid when exiting help menu
            # create_without_grid_lines(stdscr)
        elif key == ord('i'):
            write_to_cell(stdscr)
            # repaint the grid to update the new word written to the screen
            # create_without_grid_lines(stdscr)
        elif key == ord('w'):
            quick_scroll(stdscr, 'w')
        elif key == ord('a'):
            quick_scroll(stdscr, 'a')
        elif key == ord('s'):
            quick_scroll(stdscr, 's')
        elif key == ord('d'):
            quick_scroll(stdscr, 'd')
        elif key == ord(':'):
            big_commands(stdscr)
        # move the user cursor to the top left corner so if the window gets small, the cursor won't go offscreen
        if key == curses.KEY_RESIZE:
            # get dimensions again
            settings.h, settings.w = stdscr.getmaxyx()
            settings.grid_h, settings.grid_w = get_dimensions(stdscr)
            settings.current_row_idx = settings.h_holder
            settings.current_col_idx = settings.w_holder//settings.cell_w
            stdscr.move(0, 0)
        if not settings.grid_shifting and key != curses.KEY_RESIZE:
            # stdscr.refresh()
            refresh_grid(stdscr)
        else:
            create_without_grid_lines(stdscr)

if __name__ == '__main__':
    curses.wrapper(main)
