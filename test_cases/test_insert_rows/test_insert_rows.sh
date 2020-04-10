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

# insert a row at the top
python3 $program_path $data_file "testing" rr $output_file_1

# try inserting a row outside of the data, nothing should happen
python3 $program_path $data_file "testing" :7,1 rr $output_file_2
