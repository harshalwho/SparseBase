import csv

def reconstruct_matrix(parse_row_file, parse_col_file):

    # Read parse files
    with open(parse_row_file) as p_row_fh:
        row_reader = csv.reader(p_row_fh, delimiter='|')
        parse_rows = list(row_reader)[1:]

    with open(parse_col_file) as p_col_fh: 
        col_reader = csv.reader(p_col_fh, delimiter='|')
        parse_cols = list(col_reader)[1:]

    # Get labels
    row_labels = {row[1] for row in parse_rows}
    col_labels = {col[1] for col in parse_cols}

    # Map labels
    row_map = {label: i for i, label in enumerate(row_labels)}
    col_map = {label: i for i, label in enumerate(col_labels)}

    # Initialize matrix
    num_rows = len(row_labels)
    num_cols = len(col_labels)
    matrix = [[0] * num_cols for _ in range(num_rows)]

    # Fill 1s  
    for row in parse_rows:
        r_idx = row_map[row[1]]
        for c in row[2].split():
            if c in col_map:
                matrix[r_idx][col_map[c]] = 1

    # Fill 0s
    for col in parse_cols:
        c_idx = col_map[col[1]]
        for r in col[2].split(','):
            if r in row_map:  
                matrix[row_map[r]][c_idx] = 0

    return matrix


parse_row_file = 'matrix_results\ParseCol.csv'
parse_col_file = 'matrix_results\ParseRow.csv'

B = reconstruct_matrix(parse_row_file, parse_col_file)
import numpy as np
A = np.array(B)
print(A.shape)