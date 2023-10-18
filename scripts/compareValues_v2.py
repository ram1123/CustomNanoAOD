import ROOT

verbose = False

def get_values_from_tree(file_path, tree_name, branches):
    file = ROOT.TFile(file_path)
    tree = file.Get(tree_name)
    values = {branch: [] for branch in branches}

    for event in tree:
        for branch in branches:
            branch_values = []
            # split branch with  '_' and get the first element to check length
            # print ('n'+branch.split('_')[0])
            # n_values = getattr(event, 'n'+branch.split('_')[0]) if 'n'+branch.split('_')[0] in branches else 1
            n_values = getattr(event, 'n'+branch.split('_')[0])
            for i in range(n_values):
                branch_values.append(getattr(event, branch)[i])
            values[branch].append(branch_values)

    return values

file1_path = "/afs/cern.ch/user/r/rasharma/work/doubleHiggs/CustomNanoAOD/HIG-RunIISummer20UL18NanoAODv9-02546.root"
file2_path = "/afs/cern.ch/user/r/rasharma/work/doubleHiggs/CustomNanoAOD/New_30/CMSSW_10_6_30/src/HIG-RunIISummer20UL18NanoAODv9-02546_testv1.root"

# branches = ['nPhoton', 'Photon_eta', 'Photon_hoe', 'Photon_pt', 'Photon_phi', 'Photon_r9']
branches = ['Photon_eta', 'Photon_hoe', 'Photon_pt', 'Photon_phi', 'Photon_r9']
values_file1 = get_values_from_tree(file1_path, 'Events', branches)
values_file2 = get_values_from_tree(file2_path, 'Events', branches)

# Compare values
for branch in branches:
    for i, (val1, val2) in enumerate(zip(values_file1[branch], values_file2[branch])):
        if val1 != val2:
            print("Non-identical values found in event {} for variable {}".format(i+1, branch))
            print("Values from file 1: {}".format(val1))
            print("Values from file 2: {}".format(val2))
            print("---")
        if val1 == val2 and verbose:
            print("Identical values found in event {} for variable {}".format(i+1, branch))
            print("Values from file 1: {}".format(val1))
            print("Values from file 2: {}".format(val2))
            print("---")
