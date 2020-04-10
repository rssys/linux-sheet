import csv
import sys
import curses
import settings
import key_mappings
from data_management import save_data

def pop_up_help():
    h, w = 100, 100

    # manual = curses.newpad(h, w)
    manual = curses.newpad(h, w)
    manual.box()
    manual.addstr(1,2,'{:30}'.format("Linux-Sheets User Manual") + "press 'b' to go back")
    manual.addstr(3,2,"Navigation:")
    manual.addstr(4,2,'{:30}'.format("Basic Movement") + "arrow keys")
    manual.addstr(5,2,'{:30}'.format("Quick scroll(up)") + key_mappings.QUICK_UP)
    manual.addstr(6,2,'{:30}'.format("Quick scroll(down)") + key_mappings.QUICK_DOWN)
    manual.addstr(7,2,'{:30}'.format("Quick scroll(left)") + key_mappings.QUICK_LEFT)
    manual.addstr(8,2,'{:30}'.format("Quick scroll(right)") + key_mappings.QUICK_RIGHT)

    manual.addstr(10,2,"Features:")
    manual.addstr(11,2,'{:30}'.format("Insert data") + key_mappings.INSERT)
    manual.addstr(12,2,'{:30}'.format("Delete cell") + key_mappings.DELETE_CELL)
    manual.addstr(13,2,'{:30}'.format("Insert row") + key_mappings.INSERT_ROW)
    manual.addstr(14,2,'{:30}'.format("Insert column") + key_mappings.INSERT_COL)
    manual.addstr(15,2,'{:30}'.format("Delete row") + key_mappings.DELETE_ROW)
    manual.addstr(16,2,'{:30}'.format("Delete column") + key_mappings.DELETE_COL)
    manual.addstr(17,2,'{:30}'.format("Copy") + key_mappings.COPY)
    manual.addstr(18,2,'{:30}'.format("Paste") + key_mappings.PASTE)
    manual.addstr(19,2,'{:30}'.format("Undo") + key_mappings.UNDO)
    manual.addstr(20,2,'{:30}'.format("Redo") + key_mappings.REDO)
    manual.addstr(21,2,'{:30}'.format("Search") + key_mappings.SEARCH)
    manual.addstr(22,2,'{:30}'.format("Visual mode") + key_mappings.VISUAL_MODE)
    manual.addstr(23,2,'{:30}'.format("Help") + key_mappings.HELP)

    manual.addstr(25,2,"Commands that start with ':'")
    manual.addstr(26,2,'{:30}'.format("Go to") + "type: 'row, column'")
    manual.addstr(27,2,'{:30}'.format("Quit") + key_mappings.QUIT)
    manual.addstr(28,2,'{:30}'.format("Save and quit") + key_mappings.SAVE_AND_QUIT)

    manual.refresh(0, 0, 0, 0, settings.h - 1, settings.w - 1)

    exit_menu = False
    manual_y = 0
    manual_x = 0
    while True:
        key = settings.stdscr.getch()
        if key == ord(':'):
            from Clark_Sheets import write_to_bottom
            command = write_to_bottom(':')
            if command == key_mappings.SAVE_AND_QUIT:
                settings.user_exited = True
                save_data()
                break
            elif command == key_mappings.QUIT:
                settings.user_exited = True
                break
        elif key == ord('b'): #escape key
            settings.stdscr.clear()
            break
        elif key == curses.KEY_RESIZE:
            from Clark_Sheets import handle_resize
            handle_resize(key)
        manual.refresh(0, 0, 0, 0, settings.h - 1, settings.w - 1)
