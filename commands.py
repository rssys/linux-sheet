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

    def do(self, command, *args):
        args_list = [arg for arg in args]
        num_args = len(args_list)

        # TODO continue the list if you implement features with more arguments
        if num_args == 0:
            command()
        elif num_args == 1:
            command(args_list[0])
            # settings.grid.addstr(21,20, args_list[0])
        elif num_args == 2:
            command(args_list[0], args_list[1])

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

class delete_cell:
    def __init__(self):
        self.row = 0
        self.col = 0
        self.element = ''
    def __call__(self):
        self.row = settings.current_row_idx
        self.col = settings.current_col_idx
        if settings.current_row_idx < len(settings.contents) and settings.current_col_idx < len(settings.contents[0]):
            self.element = settings.contents[settings.current_row_idx][settings.current_col_idx]
            settings.contents[settings.current_row_idx][settings.current_col_idx] = ''
            settings.grid.move(settings.current_row_idx, 0);
            settings.grid.clrtoeol();

    def undo(self):
        if self.row < len(settings.contents) and self.col < len(settings.contents[0]):
            settings.contents[self.row][self.col] = self.element

def go_to(y, x):
    if y >= 0 and x >= 0:
        settings.current_row_idx = y
        settings.h_holder = y
        settings.current_col_idx = x
        settings.w_holder = x * settings.cell_w
        # determine if grid must be shifted

class insert_rows:
    def __init__(self):
        self.row = 0
        self.col = 0
        self.num_rows = ''
    def __call__(self, command_nums):
        try:
            num_rows = int(command_nums)
            self.row = settings.current_row_idx
            self.col = settings.current_col_idx
            self.num_rows = command_nums
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
    def undo(self):
        # store the user's current position
        user_rows = settings.current_row_idx
        user_cols = settings.current_col_idx
        # move to where the rows need to be deleted
        settings.current_row_idx = self.row
        settings.current_col_idx = self.col
        # delete rows
        # since the function is in the class, we need to make a dummy instance
        dr_instance = delete_rows()
        # reference the __call__function in the instance
        dr_instance(self.num_rows)
        # move the user back to original position
        settings.current_row_idx = user_rows
        settings.current_col_idx = user_cols


class insert_cols:
    def __init__(self):
        self.row = 0
        self.col = 0
        self.num_cols = ''
    def __call__(self, command_nums):
        try:
            num_cols = int(command_nums)
            self.row = settings.current_row_idx
            self.col = settings.current_col_idx
            self.num_cols = command_nums
            # only insert a col in CSV file if it is within the data we have, so if CSV file has 10 cols and user inserts col at col 200, it won't do anything
            if settings.current_col_idx < len(settings.contents[0]):
                for a in range(0, num_cols):
                    for row in settings.contents:
                        row.insert(settings.current_col_idx, '')
                settings.grid.erase()
        except ValueError:
            pass
    def undo(self):
        # store the user's current position
        user_rows = settings.current_row_idx
        user_cols = settings.current_col_idx
        # move to where the cols need to be deleted
        settings.current_row_idx = self.row
        settings.current_col_idx = self.col
        # delete cols
        # since the function is in the class, we need to make a dummy instance
        dc_instance = delete_cols()
        # reference the __call__function in the instance
        dc_instance(self.num_cols)
        # move the user back to original position
        settings.current_row_idx = user_rows
        settings.current_col_idx = user_cols

class delete_rows:
    def __init__(self):
        self.row = 0
        self.col = 0
        self.rows_data = []
    def __call__(self, command_nums):
        try:
            num_rows = int(command_nums)
            self.row = settings.current_row_idx
            self.col = settings.current_col_idx
            # only delete a row in CSV file if it is within the data we have, so if CSV file has 10 lines and user deletes row at line 200, it won't do anything
            total_rows = len(settings.contents)
            if settings.current_row_idx < total_rows:
                if settings.current_row_idx + num_rows > total_rows:
                    num_rows = total_rows - settings.current_row_idx
                for a in range(0,num_rows):
                    # save the data in the rows for undo
                    self.rows_data.append(settings.contents[settings.current_row_idx])
                    # delete the row
                    del(settings.contents[settings.current_row_idx])
                settings.grid.erase()
        except ValueError:
            pass

    def rewrite_rows(self):
        for row_index in range(0, len(self.rows_data)):
            scaled_index = settings.current_row_idx + row_index
            settings.contents.insert(scaled_index, self.rows_data[row_index])
        settings.grid.erase()

    def undo(self):
        # store the user's current position
        user_rows = settings.current_row_idx
        user_cols = settings.current_col_idx
        # move to where the rows need to be rewritten
        settings.current_row_idx = self.row
        settings.current_col_idx = self.col
        # rewrite rows
        self.rewrite_rows()
        # move the user back to original position
        settings.current_row_idx = user_rows
        settings.current_col_idx = user_cols

class delete_cols:
    def __init__(self):
        self.row = 0
        self.col = 0
        self.cols_data = []
    def __call__(self, command_nums):
        try:
            num_cols = int(command_nums)
            self.row = settings.current_row_idx
            self.col = settings.current_col_idx
            # only delete a col in CSV file if it is within the data we have, so if CSV file has 10 cols and user deletes col at col 200, it won't do anything
            total_cols = len(settings.contents[0])
            if settings.current_col_idx < total_cols:
                if settings.current_col_idx + num_cols > total_cols:
                    num_cols = total_cols - settings.current_col_idx
                for a in range(0, num_cols):
                    self.cols_data.append([])
                    for row in settings.contents:
                        # save the data in the cols for undo
                        self.cols_data[a].append(row[settings.current_col_idx])
                        # delete element in col
                        del(row[settings.current_col_idx])
                settings.grid.erase()
        except ValueError:
            pass

    def rewrite_cols(self):
        for col_index, col in enumerate(self.cols_data):
            for row_index in range(0, len(settings.contents)):
                scaled_index = settings.current_col_idx + col_index
                settings.contents[row_index].insert(scaled_index, col[row_index])
        settings.grid.erase()

    def undo(self):
        # store the user's current position
        user_rows = settings.current_row_idx
        user_cols = settings.current_col_idx
        # move to where the rows need to be rewritten
        settings.current_row_idx = self.row
        settings.current_col_idx = self.col
        # rewrite rows
        self.rewrite_cols()
        # move the user back to original position
        settings.current_row_idx = user_rows
        settings.current_col_idx = user_cols


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

class paste:
    def __init__(self):
        self.row = 0
        self.col = 0
        self.original_data = []
        for row_index, row in enumerate(settings.highlight_data):
            self.original_data.append([])
            for col in enumerate(row):
                self.original_data[row_index].append('')

    def get_original_data(self):
        for row in range(0,len(settings.highlight_data)):
            for col in range(0,len(settings.highlight_data[0])):
                scaled_row = row + self.row
                scaled_col = col + self.col
                self.original_data[row][col] = settings.contents[scaled_row][scaled_col]
                
    def __call__(self):
        content_rows = len(settings.contents)
        content_cols = len(settings.contents[0])
        required_rows = settings.current_row_idx + len(settings.highlight_data)
        required_cols = settings.current_col_idx + len(settings.highlight_data[0])
        self.row = settings.current_row_idx
        self.col = settings.current_col_idx
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
        # save the data of the block to be pasted over for undo
        self.get_original_data()
        # insert the data
        for y, row in enumerate(settings.highlight_data):
            for x, element in enumerate(row):
                settings.contents[settings.current_row_idx + y][settings.current_col_idx + x] = element

    def undo(self):
        for row in range(0,len(self.original_data)):
            for col in range(0,len(self.original_data[0])):
                # only erase data that was pasted
                scaled_row = row + self.row
                scaled_col = col + self.col
                settings.contents[scaled_row][scaled_col] = self.original_data[row][col]
        settings.grid.erase()

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
