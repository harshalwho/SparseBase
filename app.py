import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import time
import csv
import os



st.set_page_config(
    page_title= "Datawise",
    page_icon= ":white flower:",
    layout="wide",
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.cache(allow_output_mutation=True)
# Main Menu
app = option_menu(
    menu_title= "Efficient Handling of Sparse Matrix",
    options= ["Home", "Convert Matrix to DS","Retrieve Row IDs for a Column"],
    icons= ["house-fill", "envelope-paper-fill", "pc-display",],
    menu_icon= "binoculars-fill",
    default_index=0,
    orientation='horizontal',
)
#Home
if app == "Home":
    st.header("Welcome")
    st.subheader('Faster tool for handling sparse matrices')
    st.markdown('''Convert your matrix to our data structure.  
                Get lightweight files of our protocol for your matrix data.  
                Retrive specific rows for any data column in faster way''')
    # st.subheader(":moneybag:")
    #st.image(Logo, width=500)

#Convert Matrix
if app == "Convert Matrix to DS":
     st.subheader("Convert your binary matrix to lightweight files")
     tab1, tab2 = st.tabs(["Upload CSV File and Process Matrix","Get Converted lightweight files"])
     col1, col2 = st.columns(2)    
     with tab1:
         st.subheader("Please upload the Matrix you want to convert")
         st.markdown('Check whether the csv file has contains data with 0s & 1s')
         with col1:
          with st.form("dataInputForm"):
            fileName = st.text_input('Title of the Matrix')
            validity = 5
            with col2:
             file = st.file_uploader('Put the Dataset', type='csv')
             secKey = 200
             filepath = str(fileName)+' '+str(secKey)+' '+str(validity*3600)+'.csv'
            shareButton = st.form_submit_button('Convert the Matrix')


            if shareButton: 
                @st.cache_data
                def load_csv():
                    csv = pd.read_csv(file, header=None)
                    return csv
                df1 = load_csv()    

                df1.to_csv(filepath, header=False, index=False)
                st.success("The data has been recorded")
                #Read matrix            
                matrix_file = str(filepath)
                matrix = []
                with open(matrix_file) as f:
                    csv_reader = csv.reader(f)
                    for row in csv_reader:
                        matrix.append([int(x) for x in row])

                # Create directory
                dir_name = os.path.splitext(filepath)[0]
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

                # Label rows and columns
                rows = [f'R{i}' for i in range(len(matrix))]
                cols = [f'C{i}' for i in range(len(matrix[0]))]

                # Iteration counter 
                iteration = 1

                # Iterations
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
     # Get A & B
     with tab2:
          with st.form("dataOutputForm"):
            MfileName = st.text_input('Title of the concerned Matrix')
            Mvalidity = 5
            MsecKey = 200
            Mfilepath = str(MfileName)+' '+str(MsecKey)+' '+str(Mvalidity*3600)
            MshareButton = st.form_submit_button('Get the lightweight csv files')
          if MshareButton:
            if os.path.exists(Mfilepath):
                FileA = pd.read_csv(Mfilepath+'/ParseRow.csv', delimiter='|', header=None)
                st.success('Your Matrix is already converted')
                st.write('Download your files')
                @st.cache_data
                def convert_df(df):
                    return df.to_csv().encode('utf-8')
                Amat = convert_df(FileA)
                st.write('File A')
                st.download_button('Download file A', Amat, file_name='MatA',mime='text/csv')

                FileB = pd.read_csv(Mfilepath+'/ParseCol.csv', delimiter='|', header=None)
                Bmat = convert_df(FileB)
                st.write('File B')
                st.download_button('Download file B', Bmat, file_name='MatB',mime='text/csv')

            else:
                  st.error('The Matrix does not exist')

if app == 'Retrieve Row IDs for a Column':
   st.subheader('Retrieve Rows for a specific column in your binary matrix')
   with st.form('Retrieve_form'):
        RfileName = st.text_input('Title of the Matrix for which the data should be retrived')
        Rvalidity = 5
        RsecKey = 200
        Rfilepath = str(RfileName)+' '+str(RsecKey)+' '+str(Rvalidity*3600)
        RshareButton = st.form_submit_button('Connect to the Data')
        if RshareButton:
         if os.path.exists(Rfilepath):
            FileA = pd.read_csv(Rfilepath+'/ParseRow.csv', delimiter='|', header=None)
            st.success('Your Matrix is connected!')
         else:
            st.error('The Matrix does not exist')            
   ColNo = st.number_input('Enter the column for which the rows to be retrived', min_value=0, max_value=500, step=1,)
   SubCol = st.button('Check Rows for this Column')

   if SubCol:
        pin = 'C'+str(ColNo)
        X = pd.read_csv(Rfilepath+'/ParseRow.csv', delimiter='|')
        Y = pd.read_csv(Rfilepath+'/ParseCol.csv', delimiter='|') 
        Z = X.size + Y.size

        start = time.time()
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
        end = time.time()     
        if pout:
            st.success('Note down the rows as below')
            st.write(pout)
            st.write('Time taken for retrival is:', end-start,' seconds')   
            st.write('Total cells taken for storage of the matrix are:',Z)         
        else:
            st.error("The column doesn't match. Please enter valid column")

