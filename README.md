# Clark Sheets

Clark Sheets is a shell based spreadsheet application made with python3 and the curses module.

## Features

* Supports 32768 rows and 702 columns
* Copy/Paste
* Quick scroll
* Go to any coordinates on the grid
* Undo/Redo
* Insert and Delete rows/columns
* Search

## Prerequisites

python3

## Installing

install with pip

```
pip install ClarkSheets
```

You probably have multiple versions of Python installed, so you may need to specify to pip to use python3

```
python3 -m pip install ClarkSheets
```

## Using the Program

There are 2 ways to use the program:

1. You can run it with python3 on a CSV file and start using it, ex:

```
python3 Clark_Sheets.py some_file.csv
```

2. You can also pass in a series of commands as extra arguments and the program will open the file passed in, execute the passed in commands, save the data, and exit

```
python3 Clark_Sheets.py some_file.csv command1 command2
```
[key_mappings.py](https://github.com/rssys/linux-sheet/blob/master/key_mappings.py) has all the key mappings for the commands, you just have to send those in. Currently the program can only insert and delete rows and cols.

## Running the tests

Go into [test_cases](https://github.com/rssys/linux-sheet/tree/master/test_cases) and each subdirectory to run each test case(I will make a bash script to run all of them at once soon)

## Features to be added in the future

* individual resizable columns
* general resizable columns
* perhaps multiple pads to increase the dimensions this program can handle (right now I am only using one pad and it's max dimensions seem to be 32768 rows by 702 cols)
* when searching implement a next option to cycle through all matches
* customizable key key_mappings
* formulas
* Better testing, as well as testing more features such as go_to, quick_scroll, things that don't impact the data but could cause crashes because they move off screen
* when passing in extra commands, be able to write data

## Contributing

* fork
* clone
* make a new branch
* make changes
* create pull request

## Authors

Clark Chan
