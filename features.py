import csv
import sys
import curses
import settings

from dimensions import get_dimensions

def go_to(command_nums):
    coordinates = command_nums.split(',')
    row = int(coordinates[0])
    col = int(coordinates[1])
    if row >= 0 and col >= 0:
        settings.current_row_idx = row
        settings.h_holder = row
        settings.current_col_idx = col
        settings.w_holder = col * settings.cell_w
        # determine if grid must be shifted
        settings.grid_shifting = True

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
            settings.grid_shifting = True
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
            settings.grid_shifting = True
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
            settings.grid_shifting = True
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
            settings.grid_shifting = True
    except ValueError:
        pass

def highlight():
    # get smaller x and y values
    start_x = min(settings.current_col_idx, settings.highlight_start_x)
    start_y = min(settings.current_row_idx, settings.highlight_start_y)
    # get number of rows and cols to highlight
    cols_to_highlight = abs(settings.current_col_idx - settings.highlight_start_x) + 1 # the + 1 is because we always highlight start col
    rows_to_highlight = abs(settings.current_row_idx - settings.highlight_start_y) + 1 # the + 1 is because we always highlight start row
    # settings.grid.addstr(21,20,"end_x:"+str(settings.current_col_idx) + " end_y:"+ str(settings.current_row_idx))
    # settings.grid.addstr(20,20,"start_x:"+str(settings.highlight_start_x) + " start_y:"+ str(settings.highlight_start_y))
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
    start_x = min(settings.current_col_idx, settings.highlight_start_x)
    start_y = min(settings.current_row_idx, settings.highlight_start_y)
    cols = abs(settings.current_col_idx - settings.highlight_start_x) + 1 # the + 1 is because we always highlight start col
    rows = abs(settings.current_row_idx - settings.highlight_start_y) + 1 # the + 1 is because we always highlight start row
    settings.highlight_data = []
    # set up the 2d list
    for a in range(0,rows):
        settings.highlight_data.append([])
    for y in range(0, rows):
        for x in range(0,cols):
            settings.highlight_data[y].append(settings.contents[start_y+y][start_x+x])
    settings.grid.move(21,0)
    settings.grid.clrtoeol()
    settings.grid.addstr(21,20,str(settings.highlight_data))
def paste():
    pass

# TODO replace h and w with h_q_scroll and w_q_scroll later on when you decide an interval to quick scroll
def quick_scroll(stdscr, direction):
    h, w = get_dimensions(stdscr)
    if direction == 'w':
        # if user is at top of screen
        if settings.current_row_idx == settings.h_holder:
            settings.grid_shifting = True
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
            settings.grid_shifting = True
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
            settings.grid_shifting = True
            # scroll down by screen height
            settings.current_row_idx = settings.current_row_idx + h
            settings.h_holder = settings.h_holder + h
        else:
            # scroll to the bottom of screen
            settings.current_row_idx = settings.h_holder + h - 1
    else: # the character is 'd'
        if settings.current_col_idx == (settings.w_holder + w // settings.cell_w * settings.cell_w - settings.cell_w) // settings.cell_w: # we subtract settings.cell_w because we want to scroll one cell less than the full width of the screen otherwise we will go out of bounds
            settings.grid_shifting = True
            # scroll right by screen width
            settings.current_col_idx = settings.current_col_idx + w // settings.cell_w
            settings.w_holder = settings.w_holder + w // settings.cell_w * settings.cell_w # divide and multiply to truncate so that w is a multiple of cell_w
        else:
            # scroll all the way to the right of the screen
            settings.current_col_idx = (settings.w_holder + w // settings.cell_w * settings.cell_w - settings.cell_w) // settings.cell_w
