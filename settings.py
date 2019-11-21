# global variables
# the contents of the csv file
contents = []
index_dict = {}
# placeholder variables for the top left corner so we can know when to scroll
h_holder = 0
w_holder = 0
# keep track of where user is
current_row_idx = 0
current_col_idx = 0
# boolean to keep track of when to exit the program
user_exited = False
# cell width and height let us do formatted printing and navigate through each cell
cell_h = 2
cell_w = 12
# gap at top and left of screen for the bar
top_margin = 3
bottom_margin = 1
left_margin = 3
# constant to make sure we jump to the start of the word and not the edge of a cell
dist_from_wall = 1
# to keep track of where the screen is to determine if scrolling is needed
current_display_h = 0
current_display_w = 0
