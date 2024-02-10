import csv
import os

# Read matrix
matrix_file = 'sample_matrix.csv'  
matrix = []
with open(matrix_file) as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        matrix.append([int(x) for x in row])

def process_matrix(matrix):
    
    # Label rows and columns 
    rows = [f'R{i}' for i in range(len(matrix))]
    cols = [f'C{i}' for i in range(len(matrix[0]))]
    
    # Create directory
    dir_name = 'matrix_results'
    os.mkdir(dir_name)

    # Open parse files
    parse_row_file = os.path.join(dir_name, 'ParseRow.csv') 
    parse_col_file = os.path.join(dir_name, 'ParseCol.csv')
    parse_row_fh = open(parse_row_file, 'w', newline='')
    parse_col_fh = open(parse_col_file, 'w', newline='')
    parse_row_writer = csv.writer(parse_row_fh, delimiter='|')
    parse_col_writer = csv.writer(parse_col_fh, delimiter='|')

    # Write headers
    parse_row_writer.writerow(['Iteration Number', 'Rx', 'Cx'])
    parse_col_writer.writerow(['Iteration Number', 'Dx', 'Sx'])
    
    # Iteration logic
    iteration = 1
    while matrix and cols:
        
        # Find max 1s rows
        max_ones = 0
        R = []
        for i, row in enumerate(matrix):
            ones = sum(row)
            if ones > max_ones:
                max_ones = ones 
                R = [rows[i]]
            elif ones == max_ones:
                R.append(rows[i])

        # Find 0s cols only in R rows
        C = []
        for r in R:
            r_idx = rows.index(r)
            c_temp = [cols[j] for j in range(len(matrix[r_idx])) if matrix[r_idx][j] == 0]
            C.append(c_temp)
                    
        # Write to parse file
        for i in range(len(R)):
            parse_row_writer.writerow([iteration, R[i], ' '.join(C[i])])

        # Delete R rows
        R_indices = [rows.index(r) for r in R]
        matrix = [row for i,row in enumerate(matrix) if i not in R_indices]
        rows = [rows[i] for i in range(len(rows)) if i not in R_indices]
        
        # Find max 0s col and 1s rows 
        if cols:        
            max_zeros = max([sum(1-x for x in col) for col in zip(*matrix)])
            D = []
            S = []
            for j in range(len(matrix[0])):
                col = [row[j] for row in matrix]
                zeros = sum(1-x for x in col)
                if zeros == max_zeros:
                    D.append(cols[j])
                    S.append([rows[i] for i in range(len(col)) if col[i] == 1])

            # Write to parse file
            for i in range(len(D)):
                parse_col_writer.writerow([iteration, D[i], ','.join(S[i])])

            # Delete D cols
            D_indices = [cols.index(d) for d in D]
            matrix = [[row[j] for j in range(len(row)) if j not in D_indices] for row in matrix]
            cols = [cols[j] for j in range(len(cols)) if j not in D_indices]
                
        iteration += 1
 
    # Close files
    parse_row_fh.close() 
    parse_col_fh.close()
    
    return parse_row_file, parse_col_file

row_file, col_file = process_matrix(matrix)
process_matrix(matrix)