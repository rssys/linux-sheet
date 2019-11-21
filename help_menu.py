import csv
import sys
import curses
import settings
from grid_creation import create_without_grid_lines

def navigate_help_menu():
    pass

def pop_up_help(stdscr):
    h, w = stdscr.getmaxyx()
    # manual = curses.newpad(h, w)
    manual = curses.newwin(h, w)
    manual.box()
    manual.addstr(1,1,"this is the help menu")
    manual.addstr(2,1,"Navigation: Arrow keys")
    manual.addstr(3,1,"To input data: 'i', enter data")
    manual.addstr(3,1,"To input data: 'i', enter data")
    # manual.refresh(0,0,0,0,h,w)
    manual.refresh()
    exit_menu = False
    manual_y = 0
    manual_x = 0
    while True:
        key = stdscr.getch()
        navigating = False
        if key == curses.KEY_UP and manual_y > 0:
            manual_y -=1
            navigating = True
        elif key == curses.KEY_DOWN:
            manual_y += 1
            navigating = True
        elif key == curses.KEY_LEFT and manual_x > 0:
            manual_x -= 1
            navigating = True
        elif key == curses.KEY_RIGHT:
            manual_x += 1
            navigating = True
        if navigating == True:
            navigate_help_menu()
        elif key == 27: #escape key
            break
    create_without_grid_lines(stdscr)