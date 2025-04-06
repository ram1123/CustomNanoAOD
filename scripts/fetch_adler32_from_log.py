import re

# Function to extract adler32 checksum and corresponding paths from a line
# def extract_adler32_info(line, source=""):
#     adler32_pattern = r"adler32\":\"([0-9a-fA-F]+)"
#     path_pattern = r"(root://[^\s]+)"

#     adler32_match = re.search(adler32_pattern, line)
#     path_match = re.search(path_pattern, line)
#     print(f"adler32_match: {adler32_match}, path_match: {path_match}")

#     if adler32_match and path_match:
#         return adler32_match.group(1), path_match.group(1), source
#     return None, None, None

def extract_adler32_info(line, source=""):
    adler32_pattern = r"adler32\":\"([0-9a-fA-F]+)"
    path_pattern = r"([0-9a-fA-F]{8})\sroot://xcache.cms.rcac.purdue.edu"

    adler32_match = re.search(adler32_pattern, line)
    path_match = re.search(path_pattern, line)
    # print(f"adler32_match: {adler32_match}, path_match: {path_match}")

    if adler32_match:
        adler32 = adler32_match.group(1)
    else:
        adler32 = None

    if path_match:
        adler32 = path_match.group(1)
    else:
        path = None
    # print(f"adler32: {adler32}")

    return adler32

# Function to process the log file and compare adler32 checksums
def process_log_file(log_file_path):
    # Initialize variables
    das_adler32 = {}
    xcache_adler32 = {}
    mismatches = []

    # Read the log file
    with open(log_file_path, 'r') as f:
        lines = f.readlines()

    # Flags for detecting DAS and xCache blocks
    is_das_block = False
    is_xcache_block = False
    found_xcache_header = False

    # Add these variables before the loop starts
    temp_adler32 = None
    temp_path = None

    # Process each line
    for line in lines:
        if '"das' in line:
            is_das_block = True
            is_xcache_block = False
            temp_adler32, temp_path = None, None
        elif "From xcache: (Used by the code)" in line:
            found_xcache_header = True
            # print("Found xcache header")
            continue  # Skip to the next line

        if is_das_block:
            adler32_das = extract_adler32_info(line)
            # print(f"Extracted adler32_das: {adler32_das}")
            is_das_block = False  # Reset after capturing the first DAS line

        if found_xcache_header:
            # print(f"Processing xcache line: {line}")
            # Process the line to extract adler32 and path
            adler32_xcache = extract_adler32_info(line)

            found_xcache_header = False  # Reset after capturing the first xcache line


    # compare adler32 checksums
    if adler32_das and adler32_xcache:
        if adler32_das != adler32_xcache:
            mismatches.append((adler32_das, adler32_xcache))
            # print(f"Mismatch found: {adler32_das} != {adler32_xcache}")
            print(f"{log_file_path}: {adler32_das} != {adler32_xcache}")
        else:
            # print(f"Match found: {adler32_das} == {adler32_xcache}")
            pass

# Input log file path (change this to the path of your log file)
# log_file_path = '/home/shar1172/CustomNanoAOD/logs_UL2018GT36_Data_30March/nanoAOD_920540_2109.out'

# Process the log file
# process_log_file(log_file_path)

# fetch all *.out files in the directory /home/shar1172/CustomNanoAOD/logs_UL2018GT36_Data_30March
# and process each file
import os
import glob

log_directory = '/home/shar1172/CustomNanoAOD/logs_UL2018GT36_Data_30March'
log_files = glob.glob(os.path.join(log_directory, '*.out'))

for log_file in log_files:
    # print(f"Processing file: {log_file}")
    process_log_file(log_file)
