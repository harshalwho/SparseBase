import numpy as np
import csv
import pandas as pd

X = pd.read_csv('matrix_results\ParseRow.csv', delimiter='|')
Y = pd.read_csv('matrix_results\ParseCol.csv', delimiter='|')


Pin = 'C7'

def retrive_rows(Pin):

  # Parse elements in Cx and Sx columns
  X['Cx'] = X['Cx'].str.split()
  Y['Sx'] = Y['Sx'].str.split()

  # Find Pout1
  pout1 = str(Y.loc[Y['Dx'] == pin, 'Sx'].iloc[0]).strip("[]'")

  # Define itr
  itr = int(Y.loc[Y['Dx'] == pin, 'Iteration Number'])

  # Find Pout2
  mask = X['Cx'].apply(lambda x: pin not in x)
  pout2 = X.loc[X['Iteration Number'] <= itr, 'Rx'][mask].tolist()

  # Filter out NaN values
  pout1 = pout1 if pout1 != 'nan' else ''
  pout2 = [x for x in pout2 if str(x) != 'nan']

  # Concatenate Pout1 and Pout2
  pout = pout1 + ',' + ','.join(pout2)

  return pout

pin = 'C5' 
print(retrive_rows(pin))

# out = retrive_rows(pin)
# pd.DataFrame({'output': [out]}).to_csv('output.csv', index=False)