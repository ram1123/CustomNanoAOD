import ROOT

def compare_root_files(file1_path, file2_path):
    file1 = ROOT.TFile(file1_path)
    tree1 = file1.Get("Events")

    file2 = ROOT.TFile(file2_path)
    tree2 = file2.Get("Events")

    # Get list of branch names for each file
    branches1 = [b.GetName() for b in tree1.GetListOfBranches()]
    branches2 = [b.GetName() for b in tree2.GetListOfBranches()]

    # Find branches that are only in one of the files
    only_in_file1 = set(branches1) - set(branches2)
    only_in_file2 = set(branches2) - set(branches1)

    # Print the differences
    if only_in_file1:
        print "Branches only in %s:" % file1_path
        for branch in only_in_file1:
            print "  - %s" % branch

    if only_in_file2:
        print "Branches only in %s:" % file2_path
        for branch in only_in_file2:
            print "  - %s" % branch

    # Close the ROOT files
    file1.Close()
    file2.Close()

# Paths to the ROOT files you want to compare
file1_path = "/afs/cern.ch/user/r/rasharma/work/doubleHiggs/CustomNanoAOD/HIG-RunIISummer20UL18NanoAODv9-02546.root"
# file2_path = "/afs/cern.ch/user/r/rasharma/work/doubleHiggs/CustomNanoAOD/New_30/CMSSW_10_6_30/src/HIG-RunIISummer20UL18NanoAODv9-02546_testv1.root"
file2_path = "/afs/cern.ch/user/r/rasharma/work/doubleHiggs/CustomNanoAOD/New_30/CMSSW_10_6_30/src/HIG-RunIISummer20UL18NanoAODv9-02546_testv1_WithNewPhotonVars.root"

# Compare the files
compare_root_files(file1_path, file2_path)
