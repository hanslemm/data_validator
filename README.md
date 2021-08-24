# data_validator
 Compares two CSV files (which are meant to be similar, with same number of columns and pottentialy the same number of rows), outputting:
 - Shape (rows and columns) of the data files
 - Similarity between columns (that have the same name across the files)
 - Divergent columns (those with similarity < 95%) data sample (100 entries) in CLI to give a glimpse of what is diverging

 This code is very basic and will be improved according to my available time.

## Instructions
 - Clone this repo
 - Create a directory under this repo called **inputs**
 - Create the two CSV files that will be compared:
    - The files must have the same number of columns
    - The UNIQUE KEY must be the first column
    - The order of the columns must be the same across the files
    - Name the CSV file with the old output as **old.csv**
    - Name the CSV file with the new output as **new.csv**
 - Paste the CSV files **old.csv** (the old query output) and **new.csv** (the new query output) inside **inputs** directory
 - Run the program with `python validator.py` in CLI
