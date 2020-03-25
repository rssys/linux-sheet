import curses

# movement
UP = curses.KEY_UP
DOWN = curses.KEY_DOWN
RIGHT = curses.KEY_RIGHT
LEFT = curses.KEY_LEFT
QUICK_UP = 'w'
QUICK_LEFT = 'a'
QUICK_DOWN = 's'
QUICK_RIGHT = 'd'
# features
INSERT = 'i'
COPY = 'y'
PASTE = 'p'
DELETE_CELL = 'k'
SEARCH = '/'
INSERT_ROW = "rr"
DELETE_ROW = "er"
INSERT_COL = "cc"
DELETE_COL = "ec"
GOTO = "goto"
UNDO = 'u'
REDO = 'o'
# visual mode
VISUAL_MODE = 'v'
# help menu
HELP = 'h'
# exiting
QUIT = 'q'
SAVE_AND_QUIT = "wq"
