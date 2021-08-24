"""Validator"""

import os
import pandas as pd
import numpy as np

# Configure Pandas to show 100 columns
pd.options.display.max_columns = 100

# Path to the files to be analyzed
PATH_OLD = "inputs/old.csv"
PATH_NEW = "inputs/new.csv"

DIR_NAME = "outputs"

# File size limit in bytes
SIZE_LIMIT = 3_000_000_000

# Checks size limit
def over_limit():
    """
    Checks if one of the files has surpassed the allowed SIZE_LIMIT.
    """
    test1 = os.stat(PATH_OLD).st_size > SIZE_LIMIT
    test2 = os.stat(PATH_OLD).st_size > SIZE_LIMIT
    return test1 or test2


# Main routine
def main():
    """
    Main routine.
    """
    # Create target directory if don't exist
    if not os.path.exists(DIR_NAME):
        os.mkdir(DIR_NAME)

    # Open files as Pandas DataFrames
    old = pd.read_csv(PATH_OLD)
    new = pd.read_csv(PATH_NEW)

    # Check shapes
    print("### Shapes #################################################")
    print(
        f"old rows: {old.shape[0]} | "
        f"Test rows: {new.shape[0]} | "
        f"Diff.: {old.shape[0] - new.shape[0]}"
    )

    print(
        f"old cols: {old.shape[1]} | "
        f"Test cols: {new.shape[1]} | "
        f"Diff.: {old.shape[1] - new.shape[1]}"
    )
    print(" ")

    # Sets index
    old.set_index(old.columns[0], inplace=True)
    new.set_index(new.columns[0], inplace=True)

    # Rename columns in Test
    new.columns = old.columns

    # Cleans data
    old.replace("", np.nan, inplace=True)
    new.replace("", np.nan, inplace=True)
    old.fillna(0, inplace=True)
    new.fillna(0, inplace=True)

    # Compare records
    comparison = pd.DataFrame()
    key_errors = []

    for index in new.index:
        try:
            index_comparison = old.loc[index, :] == new.loc[index, :]
            comparison = comparison.append(index_comparison)
        except KeyError:
            key_errors.append(index)
            continue

    similarity = comparison.sum() / comparison.shape[0] * 100

    print("### Similarity per column ##################################")
    print(similarity)
    print(" ")

    print("### Keys not found #########################################")
    print(key_errors)
    print(
        f"--- Total: {len(key_errors)} "
        f"({len(key_errors)/new.shape[0]:.2%} of Test entries)"
    )
    print(" ")

    # Points columns that have similarity<95% to be analyzed
    check_cols = similarity[similarity < 95].index.to_list()
    check_cols_df = pd.DataFrame()
    series = {}

    # Creates a df comparing OLD column and NEW column
    for index in new.loc[~new.index.isin(key_errors)].sample(n=100).index.to_list():
        series["Key"] = index
        for col in check_cols:
            series[f"{col} [OLD]"] = old.at[index, col]
            series[f"{col} [NEW]"] = new.at[index, col]
        check_cols_df = check_cols_df.append(series, ignore_index=True)

    print("### Divergent columns comparison ############################")
    print(check_cols)
    print(check_cols_df)
    print(" ")

    # Outputs
    print("### Saving similarity table and divergent data sample #######")
    comparison.to_csv(f"{DIR_NAME}/comparison.csv")
    check_cols_df.to_csv(f"{DIR_NAME}/divergent_data_sample.csv")
    print("### Saved! ##################################################")


if over_limit() is True:
    print(f"One of the files size is bigger than the {SIZE_LIMIT} bytes accepted")
else:
    main()
