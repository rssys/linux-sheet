import csv
import sys
import curses
import settings

def save_data():
    with open('test_file_2.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(settings.contents)

def read_CSV(stdscr, file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        # get as 2d list, but sum() flattens it into 1d list
        contents = list(reader)
    return contents

def get_csv_string_format(user_input):
    return str(settings.current_row_idx) + "|" + str(settings.current_col_idx) + "|" + user_input

def write_to_cell(stdscr):
    curses.echo()
    # user_input = stdscr.getstr(current_row_idx + top_margin - h_holder, current_col_idx * cell_w + dist_from_wall + left_margin - w_holder)
    h, w = stdscr.getmaxyx()
    user_input = stdscr.getstr(h-1, 0)
    curses.noecho()
    if (str(settings.current_row_idx) + str(settings.current_col_idx)) in settings.index_dict:
        settings.contents[settings.index_dict[str(settings.current_row_idx) + str(settings.current_col_idx)]] = [get_csv_string_format(user_input)]
    else:
        settings.index_dict[str(settings.current_row_idx) + str(settings.current_col_idx)] = len(settings.contents)
        settings.contents.append([get_csv_string_format(user_input, settings.current_row_idx, settings.current_col_idx)])
    #TODO update the data
    stdscr.move(settings.current_row_idx + settings.top_margin - settings.h_holder, settings.current_col_idx * settings.cell_w + settings.dist_from_wall + settings.left_margin - settings.w_holder)
    # print index_dict
