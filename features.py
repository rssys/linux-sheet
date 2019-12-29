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

def insert_col(command_nums):
    num_cols = int(command_nums)
    # only insert a col in CSV file if it is within the data we have, so if CSV file has 10 cols and user inserts col at col 200, it won't do anything
    if settings.current_col_idx < len(settings.contents[0]):
        for a in range(0, num_cols):
            for row in settings.contents:
                row.insert(settings.current_col_idx, '')
        settings.grid_shifting = True
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
