import re

# Function to extract adler32 checksum and corresponding paths from a line
def extract_adler32_info(line, source=""):
    adler32_pattern = r"adler32\":\"([0-9a-fA-F]+)"
    path_pattern = r"(root://xcache.cms.rcac.purdue.edu[^\s]+)"

    adler32_match = re.search(adler32_pattern, line)
    path_match = re.search(path_pattern, line)

    if adler32_match:
        adler32 = adler32_match.group(1)
    else:
        adler32 = None

    if path_match:
        path = path_match.group(1)
    else:
        path = None

    return adler32, path

# Function to process the log file and find adler32 from xcache
def process_log_file(log_file_path):
    xcache_adler32 = {}
    mismatches = []

    # Read the log file
    with open(log_file_path, 'r') as f:
        lines = f.readlines()

    # Flags to detect when the "From xcache" line is encountered
    found_xcache_header = False

    # Process each line
    for line in lines:
        # Look for the "From xcache" line
        if "From xcache: (Used by the code)" in line:
            found_xcache_header = True
            continue  # Skip to the next line

        if found_xcache_header:
            # Process the line to extract adler32 and path
            adler32, path = extract_adler32_info(line)

            # If both adler32 and path are found, store them
            if adler32 and path:
                xcache_adler32[path] = adler32
            found_xcache_header = False  # Reset after capturing the first xcache line

    # Print the extracted adler32 checksum and corresponding paths
    if xcache_adler32:
        for path, adler32 in xcache_adler32.items():
            print(f"Path: {path}, Adler32: {adler32}")
    else:
        print("No matching entries found.")

# Input log file path (update with your log file path)
log_file_path = '/home/shar1172/CustomNanoAOD/logs_UL2018GT36_Data_30March/nanoAOD_920540_2109.out'

# Process the log file
process_log_file(log_file_path)
