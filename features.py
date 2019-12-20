import csv
import sys
import curses
import settings

from dimensions import get_dimensions

def go_to():
    pass

# TODO replace h and w with h_q_scroll and w_q_scroll later on when you decide an interval to quick scroll
def quick_scroll(stdscr, direction):
    h, w = get_dimensions(stdscr)
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
            # scroll to the bottom of screen
            settings.current_row_idx = settings.current_row_idx + h
            settings.h_holder = settings.h_holder + h
        else:
            # scroll down by screen height
            settings.current_row_idx = settings.h_holder + h - 1
    else: # the character is 'd'
        if settings.current_col_idx == (settings.w_holder + w // settings.cell_w * settings.cell_w - settings.cell_w) // settings.cell_w: # we subtract settings.cell_w because we want to scroll one cell less than the full width of the screen otherwise we will go out of bounds
            # scroll to the right of the screen
            settings.current_col_idx = settings.current_col_idx + w // settings.cell_w
            settings.w_holder = settings.w_holder + w // settings.cell_w * settings.cell_w # divide and multiply to truncate so that w is a multiple of cell_w
        else:
            # scroll right by screen height
            settings.current_col_idx = (settings.w_holder + w // settings.cell_w * settings.cell_w - settings.cell_w) // settings.cell_w
