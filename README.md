# data_validator
 Compares two data files (which are meant to be similar, with same number of columns and pottentialy the same number of rows), outputting:
 - Shape (rows and columns) of the data files
 - Similarity between columns (that have the same name across the files)
 - Divergent columns (those with similarity < 95%) data sample (100 entries) in CLI to give a glimpse of what is diverging
