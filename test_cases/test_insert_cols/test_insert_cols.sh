#/bin/#!/usr/bin/env bash
#!/usr/bin/python3

# store output file
output_file_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
output_file_1="${output_file_path}/actual_1"
output_file_2="${output_file_path}/actual_2"
# first navigate to test_data folder
cd ../test_data
# store that path
data_file="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
data_file+='/test_data.csv'
# navigate to main folder that contains the program
cd ../../
# store that path
program_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
program_path+='/Clark_Sheets.py'

# execute the program with the data file and insert a column
python3 $program_path $data_file "testing" cc $output_file_1

# try inserting a column outside of the data, nothing should happen
python3 $program_path $data_file "testing" :1,7 cc $output_file_2
