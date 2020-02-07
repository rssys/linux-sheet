import csv
import sys
import curses
import settings

from dimensions import get_dimensions
from printing_to_screen import print_current_location
from printing_to_screen import print_data
from printing_to_screen import print_col_letters
from printing_to_screen import print_row_numbers

def check_grid_resize():
    pass

def create_without_grid_lines():
    # need to erase to clear any strings that were previously painted that now shouldn't be there
    settings.stdscr.erase()

    # create the grid
    settings.grid = curses.newpad(1000,1000)
    # if settings.grid_h + settings.h_holder > settings.biggest_h or settings.grid_w + settings.w_holder > settings.biggest_w:
    #     settings.grid = curses.newpad(settings.grid_h + settings.h_holder, settings.grid_w + settings.w_holder)
    #     settings.biggest_h = settings.grid_h + settings.h_holder
    #     settings.biggest_w = settings.grid_w + settings.w_holder
    # settings.grid.addstr(20,settings.current_col_idx*settings.cell_w,str(settings.biggest_w))
    refresh_grid()

def refresh_grid():
    print_current_location()
    print_data()
    print_col_letters()
    print_row_numbers()
    settings.stdscr.refresh()
    # refresh pad depending on where user is and move cursor
    settings.grid.move((settings.current_row_idx), settings.dist_from_wall + (settings.current_col_idx * settings.cell_w))
    try:
        settings.grid.refresh(settings.h_holder, settings.w_holder, settings.top_margin, settings.left_margin, settings.h-settings.bottom_margin, settings.w-1)
    except curses.error:
        print(str(settings.h_holder))

# This method is outdated and if I do decide to add grid lines it will need to be update
def create_with_grid_lines():
    h, w = settings.stdscr.getmaxyx()

    # height and width of the grid window
    grid_h = h - settings.top_margin - settings.bottom_margin
    grid_w = w - settings.left_margin
    # offsets for when user scrolls down
    h_offset = 0
    w_offset = 0

    # set offsets
    if settings.current_row_idx * settings.cell_h >= grid_h:
        h_offset = settings.current_row_idx * settings.cell_h - grid_h
        h_offset += (settings.cell_h - h_offset % settings.cell_h)
    if settings.current_col_idx * settings.cell_w + settings.dist_from_wall >= grid_w:
        w_offset = settings.current_col_idx * settings.cell_w + settings.dist_from_wall - grid_w
        # print w_offset
        w_offset += (settings.cell_w - w_offset % settings.cell_w)
        # print w_offset

    # create the grid
    grid = curses.newpad(grid_h + h_offset, grid_w + w_offset)

    # loop through array
    # print data
    for row in settings.contents:
        for element in row:
            element_parts = str(element).split('|')
            y = int(element_parts[0]) * settings.cell_h
            x = int(element_parts[1]) * settings.cell_w
            element_str = element_parts[2]
            if y < grid_h + h_offset and x+settings.dist_from_wall < grid_w+w_offset:
            # if y + top_margin < grid_h + h_offset and x+dist_from_wall+left_margin < w+w_offset:
                grid.addstr(y,x+settings.dist_from_wall, element_str)

    # draw the horizontal lines
    for h_line in range(1,(grid_h+h_offset)//settings.cell_h + 1):
        y = (h_line * settings.cell_h) - 1
        grid.hline(y,0,'-',grid_w+w_offset)
    # draw the vertical lines
    for v_line in range(0,(grid_w+w_offset)//settings.cell_w + 1):
        x = (v_line * settings.cell_w)
        if x < grid_w+w_offset:
            grid.vline(0,x,'|',grid_h+h_offset)

    # refresh pad depending on where user is and move cursor
    grid.move((settings.current_row_idx * settings.cell_h), settings.dist_from_wall+(settings.current_col_idx * settings.cell_w))
    # variables for changing what portions of the screen to display
    display_h = 0
    display_w = 0

    # get display height
    if settings.current_row_idx * settings.cell_h > grid_h:
        display_h = h_offset
    else:
        if settings.current_row_idx * settings.cell_h == grid_h:
            display_h = settings.cell_h
        else:
            display_h = 0

    # get display width
    if settings.current_col_idx * settings.cell_w + settings.dist_from_wall > grid_w:
        display_w = w_offset
    else:
        if settings.current_col_idx * settings.cell_w + settings.dist_from_wall == grid_w:
            display_w = settings.cell_w
        else:
            display_w = 0

    grid.refresh(display_h,display_w,settings.top_margin,settings.left_margin,h-settings.bottom_margin,w)
