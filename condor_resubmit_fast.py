import os
import pandas as pd

def check_missing_files(input_file, output_dir):
    # Load the input file into a pandas DataFrame
    df = pd.read_csv(input_file, sep=' ', header=None, names=['configFile', 'inputMiniAOD', 'outputDirectory', 'nEvents', 'CondorLogPath'])

    # replace string "root://eos.cms.rcac.purdue.edu/" with "/eos/purdue/" in the outputDirectory column
    df['outputDirectory'] = df['outputDirectory'].str.replace("root://eos.cms.rcac.purdue.edu/", "/eos/purdue/")

    # Generate the expected output file name for each row
    df['outputNanoAODFile'] = df['inputMiniAOD'].apply(lambda x: x.split('/')[-1].replace(".root", "_NanoAOD.root"))

    # Construct the expected output file path
    df['expected_output_file'] = df['outputDirectory'] + '/' + df['outputNanoAODFile']

    # Check if each file exists
    df['file_exists'] = df['expected_output_file'].apply(os.path.exists)

    # Filter for missing files
    missing_files_df = df[df['file_exists'] == False]

    #  Get New dataframe with missing files only
    missing_files_df = missing_files_df[['configFile', 'inputMiniAOD', 'outputDirectory', 'nEvents', 'CondorLogPath']]

    # Update the outputDirectory by replacing back "/eos/purdue/" with "root://eos.cms.rcac.purdue.edu/"
    missing_files_df['outputDirectory'] = missing_files_df['outputDirectory'].str.replace("/eos/purdue/", "root://eos.cms.rcac.purdue.edu/")

    # Save the missing files to a new text file
    missing_files_df.to_csv('missing_files.txt', sep=' ', header=False, index=False)

    # Print the number of missing files
    print(f"Missing files: {len(missing_files_df)}")

    # Print the path to the new text file
    print("The list of missing files is saved to 'missing_files.txt'")


# Main function
def main():
    input_file = "HMuMu_UL2018_3Feb.txt"  # Path to your input file
    output_dir = "/eos/purdue/store/user/rasharma/customNanoAOD/UL2018/"  # Path to your output directory

    check_missing_files(input_file, output_dir)

# Run the script
if __name__ == "__main__":
    main()
