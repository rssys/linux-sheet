import csv
import sys
import curses
import settings

import key_mappings
from data_management import read_data
from data_management import save_data
from data_management import index_contents
from grid_creation import check_grid_resize
from grid_creation import create_without_grid_lines
from grid_creation import create_with_grid_lines
from grid_creation import refresh_grid
from dimensions import get_dimensions
from help_menu import pop_up_help
from commands import command_manager
from commands import write_to_cell
from commands import quick_scroll
from commands import go_to
from commands import insert_rows
from commands import insert_cols
from commands import delete_rows
from commands import delete_cols
from commands import highlight
from commands import copy
from commands import paste
from commands import search
from commands import delete_cell

def separate_command(command):
    # separate the 2 parts of the command
    command_parts = command.split(':')
    command = command_parts[0]
    command_nums = command_parts[1]
    return command, command_nums

def str_to_coordinates(str_coordinates):
    coordinates = str_coordinates.split(',')
    try:
        y = int(coordinates[0])
        x = int(coordinates[1])
        if x < 1:
            x = 1
        if y < 1:
            y = 1
        return y, x
    except ValueError:
        return -1, -1

def write_to_bottom(first_ch):
    curses.echo()
    settings.stdscr.addstr(settings.h-1,0, first_ch)
    output = settings.stdscr.getstr(settings.h-1,1).decode('utf-8')
    curses.noecho()
    settings.stdscr.clrtoeol() # this is so the command string doesn't stay on screen
    return output

def handle_colon_commands(command):
    # handle all big commands with ':'
    if command == key_mappings.SAVE_AND_QUIT:
        settings.user_exited = True
        save_data()
    elif command == key_mappings.QUIT:
        settings.user_exited = True
    elif ',' in command:
        y, x = str_to_coordinates(command)
        if y != -1 and x != -1:
            go_to(y, x)

def big_commands(arg):

    if settings.passed_commands:
        command = arg
        if ':' in command:
            # strip the colon
            command = command[1:]
            handle_colon_commands(command)
            return
    else:
        # check if user typed ':'
        if arg == ord(':'):
            command = write_to_bottom(':')
            handle_colon_commands(command)
            return
        # set command to a combination of settings.prev_key and current key
        if settings.prev_key is None:
            settings.prev_key = chr(arg)
            return
        else:
            command = settings.prev_key + chr(arg)
            # assume one of the commands match and therefore we reset previous key to nothing
            settings.prev_key = None

    # handle other big commands
    if command == key_mappings.INSERT_ROW:
        # only perform a row insert operation if number of rows in contents is less than height cap
        if len(settings.contents) < settings.grid_h_cap:
            # only insert a row in CSV file if it is within the data we have, so if CSV file has 10 lines and user inserts row at line 200, it won't do anything
            if settings.current_row_idx < len(settings.contents):
                settings.c_manager.do(insert_rows(), 1)

    elif command == key_mappings.INSERT_COL:
        # only perform a col insert operation if number of rows in contents is less than width cap
        if len(settings.contents[0]) < settings.grid_w_cap // settings.cell_w:
            # only insert a col in CSV file if it is within the data we have, so if CSV file has 10 cols and user inserts col at col 200, it won't do anything
            if settings.current_col_idx < len(settings.contents[0]):
                settings.c_manager.do(insert_cols(), 1)

    elif command == key_mappings.DELETE_ROW:
        settings.c_manager.do(delete_rows(), 1)

    elif command == key_mappings.DELETE_COL:
        settings.c_manager.do(delete_cols(), 1)

    # if we reach this else it means none of the commands happened
    else:
        # set the previous key to current key
        if not settings.passed_commands:
            settings.prev_key = chr(arg)

def handle_basic_navigation(key):
    if key == key_mappings.UP and settings.current_row_idx > 0:
        settings.current_row_idx -= 1
        if settings.current_row_idx < settings.h_holder:
            settings.h_holder -= 1
    elif key == key_mappings.DOWN:
        # need to check that we are not at the height boundary
        if settings.current_row_idx + 1 != settings.grid_h_cap:
            settings.current_row_idx += 1
            if settings.current_row_idx >= settings.h_holder + settings.grid_h:
                settings.h_holder += 1
                check_grid_resize(1,0)
            elif settings.current_row_idx >= settings.grid_total_h:
                check_grid_resize(1,0)
            # settings.stdscr.addstr(1, 0, str(settings.grid_total_h))
    elif key == key_mappings.LEFT and settings.current_col_idx > 0:
        settings.current_col_idx -= 1
        if settings.current_col_idx * settings.cell_w + settings.dist_from_wall <= settings.w_holder:
            settings.w_holder -= settings.cell_w
    elif key == key_mappings.RIGHT:
        # need to check that we are not at the width boundary
        if (settings.current_col_idx + 1) * settings.cell_w < settings.grid_w_cap:
            settings.current_col_idx += 1
            if settings.current_col_idx * settings.cell_w + settings.dist_from_wall >= settings.w_holder + settings.grid_w // settings.cell_w * settings.cell_w: # divide and multiply by cell_w to truncate and make grid_w a multiple of cell_w
                settings.w_holder += settings.cell_w
                check_grid_resize(0,1)
            elif settings.current_col_idx * settings.cell_w >= settings.grid_total_w:
                check_grid_resize(0,1)
            # settings.stdscr.addstr(1, 0, str(settings.grid_total_w))

def handle_visual_mode(key):
    if key == ord(key_mappings.VISUAL_MODE):
        settings.visual_mode = not settings.visual_mode
        if settings.visual_mode:
            settings.highlight_start_x = settings.current_col_idx
            settings.highlight_start_y = settings.current_row_idx
            settings.highlight_prev_x = settings.current_col_idx
            settings.highlight_prev_y = settings.current_row_idx
        else:
            # this is to remove the highlighting
            settings.grid.erase()

    elif key == ord(key_mappings.COPY) and settings.visual_mode:
        copy()
        settings.grid.erase()
        settings.visual_mode = False
    elif key == ord(key_mappings.PASTE):
        settings.c_manager.do(paste())

def handle_commands(key):
    # if key == ord('w'):
    if key == ord(key_mappings.QUICK_UP):
        quick_scroll(key_mappings.QUICK_UP)
    elif key == ord(key_mappings.QUICK_LEFT):
        quick_scroll(key_mappings.QUICK_LEFT)
    elif key == ord(key_mappings.QUICK_DOWN):
        quick_scroll(key_mappings.QUICK_DOWN)
    elif key == ord(key_mappings.QUICK_RIGHT):
        quick_scroll(key_mappings.QUICK_RIGHT)
    elif key == ord(key_mappings.DELETE_CELL):
        settings.c_manager.do(delete_cell())
    elif key == ord(key_mappings.SEARCH):
        search_term = write_to_bottom('/')
        settings.stdscr.clrtoeol() # this is so the command string doesn't stay on screen
        search(search_term)
    elif key == ord(key_mappings.UNDO):
        settings.c_manager.undo()
    elif key == ord(key_mappings.REDO):
        settings.c_manager.redo()
def handle_big_commands(key):
    big_commands(key)

def handle_resize(key):
    # move the user cursor to the top left corner so if the window gets small, the cursor won't go offscreen
    if key == curses.KEY_RESIZE:
        # get dimensions again
        settings.h, settings.w = settings.stdscr.getmaxyx()
        settings.grid_h, settings.grid_w = get_dimensions()
        settings.current_row_idx = settings.h_holder
        settings.current_col_idx = settings.w_holder//settings.cell_w
        # clear extra letters in letter row at top of screen
        settings.stdscr.move(2,0)
        settings.stdscr.clrtoeol()
        # clear extra row at bottom if user made window smaller
        settings.stdscr.move(settings.h-1,0)
        settings.stdscr.clrtoeol()

        # settings.stdscr.move(0, 0)
        # TODO when resizing, get out of visual mode, so we will need to unhighlight everything
        if settings.visual_mode:
            settings.visual_mode = False
            # erase the highlighted part
            settings.grid.erase()

def handle_grid_update(key):
    if settings.visual_mode:
        highlight()
        settings.highlight_prev_x = settings.current_col_idx
        settings.highlight_prev_y = settings.current_row_idx
    refresh_grid()

def handle_help_menu(key):
    if key == ord(key_mappings.HELP):
        pop_up_help()

def handle_inserting(key):
    if key == ord(key_mappings.INSERT):
        settings.c_manager.do(write_to_cell())

def main(stdscr):
    settings.stdscr = stdscr
    settings.c_manager = command_manager()
    settings.file_name = sys.argv[1]
    # set the format that the program will use (either normal CSV with commas or my own with coordinates)
    # settings.format = "my_format"
    settings.format = "CSV"
    read_data()

    # check if file exceeds max boundaries
    if settings.grid_h_cap < len(settings.contents) or settings.grid_w_cap < len(settings.contents[0] * settings.cell_w):
        sys.exit("The file you tried to open was too large")

    # determine if we are opening the program or just executing commands and then closing
    # If there are more than 2 arguments, the user is sending in commands to be done on the file
    if len(sys.argv) > 2:
        # set bool to true so when calling big commands, we can pass in commands and it will know to parse them
        settings.passed_commands = True
        testing = sys.argv[2] is "testing"
        
        if testing:
            # start iterating at the 4th argument and go through all system arguments
            for arg in sys.argv[3:]:
                big_commands(arg)
                save_data(sys.argv[-1])
        else:
            # start iterating at the 3rd argument and go through all system arguments
            for arg in sys.argv[2:]:
                big_commands(arg)
                save_data(sys.argv[1])
    # Otherwise, open the program normally with the specified file
    else:
        # set bool to true so when calling big commands, it parses user inputted command when program is running
        settings.passed_commands = False
        # create color schemes for the top and bottom margins
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # get dimensions
        settings.h, settings.w = settings.stdscr.getmaxyx()
        settings.grid_h, settings.grid_w = get_dimensions()

        # initial drawing of grid
        create_without_grid_lines()

        # we might need to resize initial grid
        if settings.grid_total_h < len(settings.contents):
            check_grid_resize(len(settings.contents) - settings.grid_total_h, 0)
        if settings.grid_total_w < len(settings.contents[0] * settings.cell_w):
            check_grid_resize(0, len(settings.contents[0]) * settings.cell_w - settings.grid_total_w)

        refresh_grid()

        # main loop
        while settings.user_exited == False:
            # read in user input
            key = settings.stdscr.getch()
            handle_visual_mode(key)
            handle_basic_navigation(key)
            handle_resize(key)
            if not settings.visual_mode:
                handle_help_menu(key)
                handle_inserting(key)
                handle_commands(key)
            handle_big_commands(key)
            handle_grid_update(key)

if __name__ == '__main__':
    curses.wrapper(main)
