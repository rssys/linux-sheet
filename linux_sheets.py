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
from features import insert_rows
from features import insert_cols
from features import insert_row
from features import insert_col
from features import delete_rows
from features import delete_cols
from features import delete_row
from features import delete_col
from features import highlight

def big_commands(stdscr):
    h, w = stdscr.getmaxyx()
    curses.echo()
    stdscr.addstr(h-1,0,":")
    command = stdscr.getstr(h-1,1).decode('utf-8')
    curses.noecho()
    if command == "wq":
        settings.user_exited = True
        save_data()
    elif command == "ir":
        insert_row("1")
    elif command == "ic":
        insert_col("1")
    elif command == "dr":
        delete_row("1")
    elif command == "dc":
        delete_col("1")
    else:
        # handle commands in the form command:line number/coordinates.
        # Examples:
        # :goto:20 means go to row 20
        # :goto:20,13 means go to row 20, column 13
        # :ir:10 means insert 10 rows at current location
        try:
            # separate the 2 parts of the command
            command_parts = command.split(':')
            command = command_parts[0]
            command_nums = command_parts[1]
            # handle each type of command
            if command == "goto":
                go_to(command_nums)
            elif command == "ir":
                insert_rows(command_nums)
            elif command == "ic":
                insert_cols(command_nums)
            elif command == "dr":
                delete_rows(command_nums)
            elif command == "dc":
                delete_cols(command_nums)
        except ValueError:
            pass
    stdscr.clrtoeol() # this is so the command string doesn't stay on screen
    # stdscr.addstr(h-1,0,str(row) + str(col))

def handle_basic_navigation(key):
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

def handle_virtual_mode(stdscr,key):
    if key == ord('v'):
        settings.visual_mode = not settings.visual_mode
        if settings.visual_mode:
            settings.highlight_start_x = settings.current_col_idx
            settings.highlight_start_y = settings.current_row_idx
            settings.highlight_prev_x = settings.current_col_idx
            settings.highlight_prev_y = settings.current_row_idx
        else:
            # this is to remove the highlighting
            create_without_grid_lines(stdscr)

def handle_features(stdscr,key):
    if key == ord('w'):
        quick_scroll(stdscr, 'w')
    elif key == ord('a'):
        quick_scroll(stdscr, 'a')
    elif key == ord('s'):
        quick_scroll(stdscr, 's')
    elif key == ord('d'):
        quick_scroll(stdscr, 'd')

def handle_big_commands(stdscr, key):
        if key == ord(':'):
            big_commands(stdscr)

def handle_resize(stdscr,key):
    # move the user cursor to the top left corner so if the window gets small, the cursor won't go offscreen
    if key == curses.KEY_RESIZE:
        # get dimensions again
        settings.h, settings.w = stdscr.getmaxyx()
        settings.grid_h, settings.grid_w = get_dimensions(stdscr)
        settings.current_row_idx = settings.h_holder
        settings.current_col_idx = settings.w_holder//settings.cell_w
        stdscr.move(0, 0)
        # TODO when resizing, get out of visual mode, so we will need to unhighlight everything
        settings.visual_mode = False

def handle_grid_update(stdscr, key):
    if not settings.grid_shifting and key != curses.KEY_RESIZE:
        # stdscr.refresh()
        if settings.visual_mode:
            highlight()
            settings.highlight_prev_x = settings.current_col_idx
            settings.highlight_prev_y = settings.current_row_idx
        refresh_grid(stdscr)
    else:
        create_without_grid_lines(stdscr)
        # settings.grid.addstr(20,20,"created GRID")
        if settings.visual_mode:
            highlight()
            settings.highlight_prev_x = settings.current_col_idx
            settings.highlight_prev_y = settings.current_row_idx
            refresh_grid(stdscr)
        # TODO we might have to rehighlight everything

def handle_help_menu(stdscr, key):
    if key == ord('h'):
        pop_up_help(stdscr)

def handle_inserting(stdscr, key):
    if key == ord('i'):
        write_to_cell(stdscr)

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
        # always reset grid_shifting to false
        settings.grid_shifting = False
        handle_virtual_mode(stdscr,key)
        handle_basic_navigation(key)
        handle_resize(stdscr,key)
        if not settings.visual_mode:
            handle_help_menu(stdscr,key)
            handle_inserting(stdscr,key)
            handle_features(stdscr,key)
        handle_big_commands(stdscr, key)
        handle_grid_update(stdscr,key)

if __name__ == '__main__':
    curses.wrapper(main)
