import pandas as pd
import numpy as np
import os

# Configure Pandas to show 100 columns
pd.options.display.max_columns = 100

# Path to the files to be analyzed
path_old = 'inputs/old.csv'
path_new = 'inputs/new.csv'

# File size limit in bytes
size_limit = 3_000_000_000

# Checks size limit
def over_limit():
  '''
  Checks if one of the files has surpassed the allowed size_limit.
  '''
  test1 = os.stat(path_old).st_size > size_limit
  test2 = os.stat(path_old).st_size > size_limit
  return (test1 or test2)

# Main routine
def main():
  '''
  Main routine.
  '''
  old = pd.read_csv(path_old)
  new = pd.read_csv(path_new)

  # Check shapes
  print('### Shapes #################################################')
  print(
    f'old rows: {old.shape[0]} | '
    f'Test rows: {new.shape[0]} | '
    f'Diff.: {old.shape[0] - new.shape[0]}'
  )

  print(
    f'old cols: {old.shape[1]} | '
    f'Test cols: {new.shape[1]} | '
    f'Diff.: {old.shape[1] - new.shape[1]}'
  )
  print(' ')

  # Sets index
  old.set_index(old.columns[0], inplace= True)
  new.set_index(new.columns[0], inplace= True)

  # Rename columns in Test
  new.columns = old.columns

  # Cleans data
  old.replace('', np.nan, inplace=True)
  new.replace('', np.nan, inplace=True)
  old.fillna(0, inplace=True)
  new.fillna(0, inplace=True)

  # Compare records
  comparison = pd.DataFrame()
  keyErrors = []

  for index in new.index:
      try:
        index_comparison = old.loc[index,:] == new.loc[index,:]
        comparison = comparison.append(index_comparison)
      except KeyError:
        keyErrors.append(index)
        continue

  similarity = comparison.sum()/comparison.shape[0]*100

  print('### Similarity per column ##################################')
  print(similarity)
  print(' ')

  print('### Keys not found #########################################')
  print(keyErrors)
  print(
    f'--- Total: {len(keyErrors)} ' \
    f'({len(keyErrors)/new.shape[0]:.2%} of Test entries)'
  )
  print(' ')

  # Points columns that have similarity<95% to be analyzed
  check_cols = similarity[similarity<95].index.to_list()
  check_cols_df = pd.DataFrame()
  series = {}

  # Creates a df comparing OLD column and NEW column
  for index in new.loc[
    ~new.index.isin(keyErrors)
    ].sample(n=100).index.to_list():
    for col in check_cols:
      series[f'{col} [OLD]'] = old.at[index,col]
      series[f'{col} [NEW]'] = new.at[index,col]
    check_cols_df=check_cols_df.append(series, ignore_index=True)

  print('### Divergent columns comparison ############################')
  print(check_cols)
  print(check_cols_df)
  print(' ')

  # Outputs
  print('### Saving similarity table and divergent data sample #######')
  comparison.to_csv('output/comparison.csv')
  check_cols_df.to_csv('output/divergent_data_sample.csv')

if over_limit() == True:
  print(
    f'One of the files size is bigger than the {size_limit} bytes accepted'
  )
else:
  main()