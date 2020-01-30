import csv
import sys
import curses
import settings
from abc import ABC, abstractmethod

from dimensions import get_dimensions
from data_management import pad_data_with_commas
from data_management import extend_rows
from data_management import extend_cols


class command_manager:
    def __init__(self):
        self.undo_commands = []
        self.redo_commands = []
    def push_undo_command(self, command):
        self.undo_commands.append(command)
    def pop_undo_command(self):
        # try:
        #     last_undo_command = self.undo_commands.pop()
        # except IndexError:
        #     raise EmptyCommandStackError()
        # return last_undo_command
        last_undo_command = self.undo_commands.pop()
        return last_undo_command

    def push_redo_command(self, command):
        self.redo_commands.append(command)

    def pop_redo_command(self):
        try:
            last_redo_command = self.redo_commands.pop()
        except IndexError:
            raise EmptyCommandStackError()
        return last_redo_command

    def do(self, command):
        command()
        self.push_undo_command(command)
        # clear the redo stack when a new command was executed
        self.redo_commands[:] = []

    def undo(self, n=1):
        for _ in range(n):
            if len(self.undo_commands) != 0:
                command = self.pop_undo_command()
                command.undo()
                self.push_redo_command(command)
            else:
                # TODO print to the screen that there are no more commands to undo
                pass
    def redo(self, n=1):
        for _ in range(n):
            if len(self.redo_commands) != 0:
                command = self.pop_redo_command()
                command()
                self.push_undo_command(command)
            else:
                # TODO print to the screen that there are no more commands to redo
                pass

class write_to_cell:
    def __init__(self):
        self.row = 0
        self.col = 0
    def __call__(self):
        self.row = settings.current_row_idx
        self.col = settings.current_col_idx

        curses.echo()
        # user_input = settings.stdscr.getstr(current_row_idx + top_margin - h_holder, current_col_idx * cell_w + dist_from_wall + left_margin - w_holder)
        h, w = settings.stdscr.getmaxyx()
        user_input = settings.stdscr.getstr(h-1, 0)
        # return if the string was empty
        if not user_input:
            return
        curses.noecho()
        if settings.format == "my_format":
            if (str(settings.current_row_idx) + str(settings.current_col_idx)) in settings.index_dict:
                settings.contents[settings.index_dict[str(settings.current_row_idx) + str(settings.current_col_idx)]] = [get_csv_string_format(user_input)]
            else:
                settings.index_dict[str(settings.current_row_idx) + str(settings.current_col_idx)] = len(settings.contents)
                settings.contents.append([get_csv_string_format(user_input)])
            settings.stdscr.move(settings.current_row_idx + settings.top_margin - settings.h_holder, settings.current_col_idx * settings.cell_w + settings.dist_from_wall + settings.left_margin - settings.w_holder)
        else:
            while len(settings.contents) <= settings.current_row_idx:
                settings.contents.append([])
            while len(settings.contents[settings.current_row_idx]) <= settings.current_col_idx:
                settings.contents[settings.current_row_idx].append('')
            settings.contents[settings.current_row_idx][settings.current_col_idx] = user_input.decode('utf-8')
            pad_data_with_commas()
        settings.stdscr.clrtoeol()
        settings.grid.move((settings.current_row_idx), settings.dist_from_wall + (settings.current_col_idx * settings.cell_w))
        settings.grid.clrtoeol()

    def undo(self):
        settings.contents[self.row][self.col] = ''
        settings.grid.move((self.row), settings.dist_from_wall + (self.col * settings.cell_w))
        settings.grid.clrtoeol()

def delete_cell():
    if settings.current_row_idx < len(settings.contents) and settings.current_col_idx < len(settings.contents[0]):
        settings.contents[settings.current_row_idx][settings.current_col_idx] = '';
        settings.grid.move(settings.current_row_idx, 0);
        settings.grid.clrtoeol();

def go_to(y, x):
    if y >= 0 and x >= 0:
        settings.current_row_idx = y
        settings.h_holder = y
        settings.current_col_idx = x
        settings.w_holder = x * settings.cell_w
        # determine if grid must be shifted

def insert_row(command_nums):
    insert_rows(command_nums)

def insert_col(command_nums):
    insert_cols(command_nums)

def insert_rows(command_nums):
    try:
        num_rows = int(command_nums)
        # only insert a row in CSV file if it is within the data we have, so if CSV file has 10 lines and user inserts row at line 200, it won't do anything
        if settings.current_row_idx < len(settings.contents):
            row_len = len(settings.contents[0])
            row = []
            for comma in range(0, row_len):
                row.append('')
            for a in range(0, num_rows):
                settings.contents.insert(settings.current_row_idx, row)
            settings.grid.erase()
    except ValueError:
        pass

def insert_cols(command_nums):
    try:
        num_cols = int(command_nums)
        # only insert a col in CSV file if it is within the data we have, so if CSV file has 10 cols and user inserts col at col 200, it won't do anything
        if settings.current_col_idx < len(settings.contents[0]):
            for a in range(0, num_cols):
                for row in settings.contents:
                    row.insert(settings.current_col_idx, '')
            settings.grid.erase()
    except ValueError:
        pass

def delete_row(command_nums):
    delete_rows(command_nums)

def delete_col(command_nums):
    delete_cols(command_nums)

def delete_rows(command_nums):
    try:
        num_rows = int(command_nums)
        # only delete a row in CSV file if it is within the data we have, so if CSV file has 10 lines and user deletes row at line 200, it won't do anything
        total_rows = len(settings.contents)
        if settings.current_row_idx < total_rows:
            if settings.current_row_idx + num_rows > total_rows:
                num_rows = total_rows - settings.current_row_idx
            for a in range(0,num_rows):
                del(settings.contents[settings.current_row_idx])
            settings.grid.erase()

    except ValueError:
        pass

def delete_cols(command_nums):
    try:
        num_cols = int(command_nums)
        # only delete a col in CSV file if it is within the data we have, so if CSV file has 10 cols and user deletes col at col 200, it won't do anything
        total_cols = len(settings.contents[0])
        if settings.current_col_idx < total_cols:
            if settings.current_col_idx + num_cols > total_cols:
                num_cols = total_cols - settings.current_col_idx
            for a in range(0, num_cols):
                for row in settings.contents:
                    del(row[settings.current_col_idx])
            settings.grid.erase()
    except ValueError:
        pass

def get_highlight_coordinates():
    # get smaller x and y values
    start_x = min(settings.current_col_idx, settings.highlight_start_x)
    start_y = min(settings.current_row_idx, settings.highlight_start_y)
    # get number of rows and cols to highlight
    cols_to_highlight = abs(settings.current_col_idx - settings.highlight_start_x) + 1 # the + 1 is because we always highlight start col
    rows_to_highlight = abs(settings.current_row_idx - settings.highlight_start_y) + 1 # the + 1 is because we always highlight start row
    return start_x, start_y, cols_to_highlight, rows_to_highlight

def highlight():
    start_x, start_y, cols_to_highlight, rows_to_highlight = get_highlight_coordinates()
    # get ending coordinates
    end_x = start_x + cols_to_highlight
    end_y = start_y + rows_to_highlight
    for row in range(start_y, end_y):
        for col in range(start_x, end_x):
            settings.grid.chgat(row, col * settings.cell_w, settings.cell_w, curses.A_REVERSE)
    # get rid of excess highlighting if necessary
    if settings.highlight_prev_x < start_x or settings.highlight_prev_x >= end_x:
        for row in range(start_y, end_y):
            settings.grid.chgat(row, settings.highlight_prev_x * settings.cell_w, settings.cell_w, curses.A_NORMAL)
    elif settings.highlight_prev_y < start_y or settings.highlight_prev_y >= end_y:
        for col in range(start_x, end_x):
            settings.grid.chgat(settings.highlight_prev_y, col * settings.cell_w, settings.cell_w, curses.A_NORMAL)

def copy():
    start_x, start_y, cols, rows = get_highlight_coordinates()
    settings.highlight_data = []
    # set up the 2d list
    for a in range(0,rows):
        settings.highlight_data.append([])
    for y in range(0, rows):
        for x in range(0,cols):
            if start_y+y < len(settings.contents) and start_x+x < len(settings.contents[0]):
                settings.highlight_data[y].append(settings.contents[start_y+y][start_x+x])
    # settings.grid.move(21,0)
    # settings.grid.clrtoeol()
    # settings.grid.addstr(21,20,str(settings.highlight_data))

def paste():
    content_rows = len(settings.contents)
    content_cols = len(settings.contents[0])
    required_rows = settings.current_row_idx + len(settings.highlight_data)
    required_cols = settings.current_col_idx + len(settings.highlight_data[0])
    if required_rows > content_rows and required_cols <= content_cols:
        extend_rows(content_rows, required_rows)
        pad_data_with_commas()
    elif required_rows <= content_rows and required_cols > content_cols:
        extend_cols(content_cols, required_cols)
        pad_data_with_commas()
    elif required_rows > content_rows and required_cols > content_cols:
        extend_cols(content_cols, required_cols)
        extend_rows(content_rows, required_rows)
        pad_data_with_commas()
    # insert the data
    for y, row in enumerate(settings.highlight_data):
        for x, element in enumerate(row):
            settings.contents[settings.current_row_idx + y][settings.current_col_idx + x] = element

def search(search_term):
    for y, row in enumerate(settings.contents):
        for x, element in enumerate(row):
            if element == search_term:
                go_to(y, x)

# TODO replace h and w with h_q_scroll and w_q_scroll later on when you decide an interval to quick scroll
def quick_scroll(direction):
    h, w = get_dimensions()
    if direction == 'w':
        # if user is at top of screen
        if settings.current_row_idx == settings.h_holder:
            if settings.current_row_idx - h <= 0:
                # scroll all the way up since we scroll less than screen height
                settings.current_row_idx = 0
                settings.h_holder = 0
            else:
                # scroll up by screen height
                settings.current_row_idx = settings.current_row_idx - h
                settings.h_holder = settings.h_holder - h
        else:
            # go to the top of the screen
            settings.current_row_idx = settings.h_holder
    elif direction == 'a':
        if settings.current_col_idx == settings.w_holder // settings.cell_w:
            if settings.current_col_idx - w // settings.cell_w <= 0:
                # scroll all the way left since we scroll less than screen width
                settings.current_col_idx = 0
                settings.w_holder = 0
            else:
                # scroll left by screen width
                settings.current_col_idx = settings.current_col_idx - w // settings.cell_w
                settings.w_holder = settings.w_holder - w // settings.cell_w * settings.cell_w # divide and multiply to truncate so that w is a multiple of cell_w
        else:
            settings.current_col_idx = settings.w_holder // settings.cell_w
    elif direction == 's':
        if settings.current_row_idx == settings.h_holder + h - 1:
            # scroll down by screen height
            settings.current_row_idx = settings.current_row_idx + h
            settings.h_holder = settings.h_holder + h
        else:
            # scroll to the bottom of screen
            settings.current_row_idx = settings.h_holder + h - 1
    else: # the character is 'd'
        if settings.current_col_idx == (settings.w_holder + w // settings.cell_w * settings.cell_w - settings.cell_w) // settings.cell_w: # we subtract settings.cell_w because we want to scroll one cell less than the full width of the screen otherwise we will go out of bounds
            # scroll right by screen width
            settings.current_col_idx = settings.current_col_idx + w // settings.cell_w
            settings.w_holder = settings.w_holder + w // settings.cell_w * settings.cell_w # divide and multiply to truncate so that w is a multiple of cell_w
        else:
            # scroll all the way to the right of the screen
            settings.current_col_idx = (settings.w_holder + w // settings.cell_w * settings.cell_w - settings.cell_w) // settings.cell_w
