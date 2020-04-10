import csv
import sys
import curses
import settings

# this is a method for using my own format with coordinates
def index_contents():
    for index, element in enumerate(settings.contents):
        element_parts = str(element).split('|')
        y = element_parts[0][2:] #we have to take from the second index because for some reason each element has the bracket and single quotes included
        x = element_parts[1]
        # settings.stdscr.move(0,0)
        # settings.stdscr.addstr(str(y))
        # break
        settings.index_dict[y + x] = index

def save_data(*args):
    # if no args passed, save data normally with settings.file_name
    if len(args) == 0:
        with open(settings.file_name, 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(settings.contents)
    # if there is an argument, then it is an output_file to put actual testcase data
    else:
        with open(args[0], 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(settings.contents)

def read_data():
    # with open(settings.file_name, 'r') as file:
    try:
        file = open(settings.file_name, 'r')
        reader = csv.reader(file, delimiter=',')
        # get as 2d list, but sum() flattens it into 1d list
        settings.contents = list(reader)
        # if settings.contents is empty, add a single empty character to prevent bugs(in case user inserts rows or something)
        if len(settings.contents) == 0:
            settings.contents.insert(0,[])
    except FileNotFoundError:
        # create a new file
        file = open(settings.file_name, 'x')
        settings.contents = [[]]

    # If using my format then we need to index corrdinates, otherwise handle with regular csv with just commas
    if settings.format == "my_format":
        index_contents()
    else:
        # align contents so that each row has same length (pad with commas)
        pad_data_with_commas()

def get_csv_string_format(user_input):
    return str(settings.current_row_idx) + "|" + str(settings.current_col_idx) + "|" + user_input

def extend_rows(content_rows, required_rows):
    while required_rows > 0 and len(settings.contents) < settings.grid_total_h:
        settings.contents.append([])
        required_rows -= 1

def extend_cols(content_cols, required_cols):
    # for a in range(content_cols, required_cols):
    #     settings.contents[0].append('')
    while required_cols > 0 and len(settings.contents[0]) < settings.grid_total_w // settings.cell_w:
        settings.contents[0].append('')
        required_cols -= 1

# everytime we write to a cell using regular CSV format we have to check if we need to pad commas so each row is the same length
def pad_data_with_commas():
    max_len = max(len(x) for x in settings.contents)
    for index, element in enumerate(settings.contents):
        current_row_len =len(element)
        for y in range(current_row_len, max_len):
            settings.contents[index].append('')

def write_to_cell():
    curses.echo()
    # user_input = settings.stdscr.getstr(current_row_idx + top_margin - h_holder, current_col_idx * cell_w + dist_from_wall + left_margin - w_holder)
    h, w = settings.stdscr.getmaxyx()
    user_input = settings.stdscr.getstr(h-1, 0)
    # return if the string was empty
    if not user_input:
        return
    curses.noecho()
    if settings.format == "my_format":
        if (str(settings.current_row_idx) + str(settings.current_col_idx)) in settings.index_dict:
            settings.contents[settings.index_dict[str(settings.current_row_idx) + str(settings.current_col_idx)]] = [get_csv_string_format(user_input)]
        else:
            settings.index_dict[str(settings.current_row_idx) + str(settings.current_col_idx)] = len(settings.contents)
            settings.contents.append([get_csv_string_format(user_input)])
        settings.stdscr.move(settings.current_row_idx + settings.top_margin - settings.h_holder, settings.current_col_idx * settings.cell_w + settings.dist_from_wall + settings.left_margin - settings.w_holder)
    else:
        while len(settings.contents) <= settings.current_row_idx:
            settings.contents.append([])
        while len(settings.contents[settings.current_row_idx]) <= settings.current_col_idx:
            settings.contents[settings.current_row_idx].append('')
        settings.contents[settings.current_row_idx][settings.current_col_idx] = user_input.decode('utf-8')
        pad_data_with_commas()
    settings.stdscr.clrtoeol()
    settings.grid.move((settings.current_row_idx), settings.dist_from_wall + (settings.current_col_idx * settings.cell_w))
    settings.grid.clrtoeol()
