import pandas as pd
from scipy.stats import spearmanr
import sys

def correlation_analysis(input_file1, input_file2, output_file):
    matrix1 = pd.read_csv(input_file1, delimiter='\t')
    matrix2 = pd.read_csv(input_file2, delimiter='\t')

    transcript_ids1 = matrix1.iloc[:, 0]
    transcript_ids2 = matrix2.iloc[:, 0]

    if len(transcript_ids1) != len(transcript_ids2):
        print("Error! Number of rows in the two matrices must be the same.")
        sys.exit(1)

    # Initialize
    correlation_results = []
    dropped_rows = []

    for i in range(len(transcript_ids1)):
        row_matrix1 = matrix1.iloc[i, 1:]
        row_matrix2 = matrix2.iloc[i, 1:]

        # Check for rows with missing data
        if row_matrix1.isnull().all() or row_matrix2.isnull().all():
            dropped_rows.append(transcript_ids1.iloc[i])
            continue

        # Check for constant rows
        if row_matrix1.nunique() == 1 or row_matrix2.nunique() == 1:
            dropped_rows.append(transcript_ids1.iloc[i])
            continue

        concat_id = transcript_ids1.iloc[i] + '_' + transcript_ids2.iloc[i]
        correlation_coefficient, p_value = spearmanr(row_matrix1, row_matrix2)
        r_square = correlation_coefficient ** 2
        correlation_results.append([concat_id, correlation_coefficient, p_value, r_square])

    result_df = pd.DataFrame(correlation_results, columns=['Transcript_ID', 'Correlation_Coefficient', 'P_Value', 'R_Square'])

    result_df.to_csv(output_file, index=False, sep='\t')
    
    # Display dropped rows
    if dropped_rows:
        print(f"Dropped Rows (due to missing or constant data): {dropped_rows}")
    else:
        print("No rows were dropped due to missing or constant data.")

    print(f"Pairwise correlation analysis results (Spearman) saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 4 or sys.argv[1] == '--help':
        print("Usage: python script.py <input_file1> <input_file2> <output_file>")
        sys.exit(1)

    input_file1 = sys.argv[1]
    input_file2 = sys.argv[2]
    output_file = sys.argv[3]

    correlation_analysis(input_file1, input_file2, output_file)
