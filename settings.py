# global variables
# window object representing the entire screen
settings.stdscr = None
# the name of the file we are editing
file_name = ""
# the format to be used, this will either be regular CSV with commas or my own format with coordinates attached
format = ""
# the contents of the csv file
contents = []
# this dictionary is for my own format where each input has coordinates attached to it
index_dict = {}
# the grid object that will hold all the contents
grid = None
# height and width of the screen
h = 0
w = 0
# grid height and width
grid_h = 0
grid_w = 0
# placeholder variables for the top left corner so we can know when to scroll
h_holder = 0
w_holder = 0
# keep track of the biggest the window has gotten so we only recreate the grid if it gets bigger
biggest_h = 0
biggest_w = 0
# keep track of where user is
current_row_idx = 0
current_col_idx = 0
# boolean to keep track of when to exit the program
user_exited = False
# cell width and height let us do formatted printing and navigate through each cell
cell_h = 2
cell_w = 12
# gap at top, bottom, and left of screen for the row and column bars and for when user enters input
top_margin = 3
bottom_margin = 1
left_margin = 3
# constant to make sure we jump to the start of the word and not the edge of a cell
dist_from_wall = 1
# to keep track of where the screen is to determine if scrolling is needed
current_display_h = 0
current_display_w = 0
# number of rows and cols to quick scroll
# TODO use these, right now I am just scrolling by the screen height and width
h_q_scroll = 0
w_q_scroll = 0
# boolean for whether or not visual mode is active (for highlighting, copy/paste)
visual_mode = False
# coordinates for where the user entered visual mode
highlight_start_x = 0
highlight_start_y = 0
# coordinates for where the user exited visual mode
highlight_end_x = 0
highlight_end_y = 0
# to get rid of excess highlighting, we need to keep track of the previous coordinates
highlight_prev_x = 0
highlight_prev_y = 0
# this 2d list is for storing the data that the user highlights
highlight_data = []
