import csv
import sys
import curses
import settings

def get_dimensions():

    # height and width of the grid window
    grid_h = settings.h - settings.top_margin - settings.bottom_margin
    grid_w = settings.w - settings.left_margin
    return grid_h, grid_w
