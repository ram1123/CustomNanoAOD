import ROOT

def compare_photon_branches(file1_path, file2_path):
    file1 = ROOT.TFile(file1_path)
    tree1 = file1.Get("Events")

    file2 = ROOT.TFile(file2_path)
    tree2 = file2.Get("Events")

    # Get list of branch names for each file that start with 'Photon_'
    branches1 = [b.GetName() for b in tree1.GetListOfBranches() if b.GetName().startswith('Photon_')]
    branches2 = [b.GetName() for b in tree2.GetListOfBranches() if b.GetName().startswith('Photon_')]

    # Find branches that are only in one of the files
    only_in_file1 = set(branches1) - set(branches2)
    only_in_file2 = set(branches2) - set(branches1)

    # Print the differences
    if only_in_file1:
        print "Branches starting with 'Photon_' only in %s:" % file1_path
        for branch in only_in_file1:
            print "  - %s" % branch

    if only_in_file2:
        print "Branches starting with 'Photon_' only in %s:" % file2_path
        for branch in only_in_file2:
            print "  - %s" % branch

    # Close the ROOT files
    file1.Close()
    file2.Close()

# Paths to the ROOT files you want to compare
file1_path = "/afs/cern.ch/user/r/rasharma/work/doubleHiggs/CustomNanoAOD/New_30/CMSSW_10_6_30/src/HIG-RunIISummer20UL18NanoAODv9-02546_testv1.root"
file2_path = "805455c8-92ee-4881-a132-1a4c8737c9a6.root"

# Compare the files
compare_photon_branches(file1_path, file2_path)
