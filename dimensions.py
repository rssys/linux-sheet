import csv
import sys
import curses
import settings

def get_dimensions(stdscr):
    h, w = stdscr.getmaxyx()

    # height and width of the grid window
    grid_h = h - settings.top_margin - settings.bottom_margin
    grid_w = w - settings.left_margin
    return grid_h, grid_w
