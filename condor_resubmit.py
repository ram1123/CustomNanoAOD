import os
from ROOT import TFile
from Resubmit_template import jdl_part_1, jdl_part_2

"""Condor resubmit script.

# Three steps to submit condor script

1. Get the list of jobs from the condor jdl file and the expected output root files
2. Get the list of output root files from the output directory
   1. Check if these root files are good and have entries, if not, makr them as bad or remove them from the correct output root file list
3. Compare the two lists and find the missing root files
4. Get a list of jobs to be submitted from step 2 and 3.
5. Prepare a new condor jdl file with the list of jobs from step 4.
6. Submit the new condor jdl file.
"""

def get_map_from_stdout_files(cluster_id, log_path):
    """Get the map from all *.stdout files based on two strings: "Input MiniAOD File" and "Output NanoAOD File".

    Args:
        cluster_id (int): Condor cluster ID.
        log_path (str): Path to the log files.

    Returns:
        dict: Map from all *.stdout files based on two strings: "Input MiniAOD File" and "Output NanoAOD File".
    """
    map = {}
    outfiltlist = []
    for file in os.listdir(log_path):
        if file.endswith(".stdout") and str(cluster_id) in file:
            print("file: {0}".format(file))
            with open(os.path.join(log_path, file)) as f:
                datafile = f.readlines()
                for line in datafile:
                    if "Input MiniAOD File" in line:
                        split_line = line.split()
                        infile = split_line[-1]
                    elif "Output NanoAOD File" in line:
                        split_line = line.split()
                        outfile = split_line[-1]
                        outfiltlist.append(outfile)
                map[outfile] = infile
                print("infile: {0}, outfile: {1}".format(infile, outfile))
                print("map: {0}".format(map)  )
    return outfiltlist, map

def get_root_files_from_dir(directory):
    """Get the list of output root files from the output directory.

    Args:
        directory (str): Path to the output directory.

    Returns:
        list: List of output root files.
    """
    flist = os.listdir(directory)
    RootFlist = [fname for fname in flist if '.root' in fname]

    # check if they are not corrupted and have entries
    filelist_to_remove = []
    for file in RootFlist:
      tfile = None
      print('Checking file: '+directory+'/'+file)
      try:
        tfile = TFile.Open(directory+'/'+file);
      except:
        pass
      print('File is open: {}'.format(tfile))
      if tfile:
        if (tfile.IsZombie()):
          filelist_to_remove.append(file)
      else:
        print('File could not be opened, adding it to missing files')
        filelist_to_remove.append(file)

    print('Removing the following files from the list of root files: ')
    print(filelist_to_remove)
    RootFlist = [fname for fname in RootFlist if fname not in filelist_to_remove]
    return RootFlist

def get_missing_files(job_list, root_file_list):
    """Compare the two lists and find the missing root files.

    Args:
        job_list (list): List of jobs.
        root_file_list (list): List of output root files.

    Returns:
        list: List of missing root files.
    """
    missing = []
    for job in job_list:
        if job not in root_file_list:
            missing.append(job)
    return missing


def prepare_new_jdl_file(jdl_file, job_list_to_submit, map_out_in_files):
    """Prepare a new condor jdl file with the list of jobs from step 4.

    Args:
        jdl_file (str): Path to the condor jdl file.
        job_list_to_submit (list): List of jobs to be submitted.
    """
    with open(jdl_file.replace('.jdl','_resubmit1.jdl'), "w") as f:
        f.write(jdl_part_1)
        for job in job_list_to_submit:
            f.write(jdl_part_2.format(Infile=map_out_in_files[job], ResubmitString="Resubmit1"))
            f.write("\n")


def submit_new_jdl_file(jdl_file):
    """Submit the new condor jdl file.

    Args:
        jdl_file (str): Path to the condor jdl file.
    """
    bashCommand = "condor_submit %s"%(jdl_file)
    os.system(bashCommand)

def main():
    """Main function.
    """
    jdl_file = "HH_WWgg_Signal_v2.jdl"
    output_dir = "/eos/user/r/rasharma/post_doc_ihep/double-higgs/nanoAODnTuples/nanoAOD_20Oct2023/UL2018/EGamma_Run2018A/"

    outfilelist, map_out_in_files = get_map_from_stdout_files(6337236, "logs/UL2018/EGamma_Run2018A/")

    root_file_list = get_root_files_from_dir(output_dir)
    print("output_dir: {0}".format(output_dir))
    print("root_file_list: {0}".format(root_file_list))
    missing = get_missing_files(outfilelist, root_file_list)
    print("missing: {0}".format(missing))
    prepare_new_jdl_file(jdl_file, missing, map_out_in_files)
    # submit_new_jdl_file(jdl_file)

if __name__ == "__main__":
    main()
