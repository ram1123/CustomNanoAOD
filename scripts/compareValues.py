import ROOT

# List of ROOT file paths
file_paths = [
    "/afs/cern.ch/user/r/rasharma/work/doubleHiggs/CustomNanoAOD/HIG-RunIISummer20UL18NanoAODv9-02546.root",
    "/afs/cern.ch/user/r/rasharma/work/doubleHiggs/CustomNanoAOD/New_30/CMSSW_10_6_30/src/HIG-RunIISummer20UL18NanoAODv9-02546_testv1.root"
]

# Lists to store photon pt values from each file
photon_pts_file1 = []
photon_pts_file2 = []

# Loop over all file paths to read the data into lists
for idx, file_path in enumerate(file_paths):
    # Open the ROOT file
    root_file = ROOT.TFile.Open(file_path)

    # Check if file is opened successfully
    if not root_file or root_file.IsZombie():
        print("Error opening file: {}".format(file_path))
        continue

    # Get the TTree from the ROOT file
    tree = root_file.Get("Events")

    # Check if tree exists
    if not tree:
        print("TTree not found in file: {}".format(file_path))
        continue

    print("Reading data from file: {}".format(file_path))

    # Loop over all events in the tree
    for event in tree:
        # Access the photon pt values for this event
        nPhotons = event.nPhoton
        photon_pts = [event.Photon_pt[i] for i in range(nPhotons)]

        # Store the photon pt values in corresponding list
        if idx == 0:
            photon_pts_file1.append(photon_pts)
        else:
            photon_pts_file2.append(photon_pts)

    # Close the ROOT file
    root_file.Close()

# Now compare the photon pt values event-by-event
# for i, (pts1, pts2) in enumerate(zip(photon_pts_file1, photon_pts_file2)):
#     print("Comparing event {}".format(i+1))
#     print("Photon pt values from file 1: {}".format(pts1))
#     print("Photon pt values from file 2: {}".format(pts2))

#     if pts1 == pts2:
#         print("Photon pt values are identical for this event.")
#     else:
#         print("Photon pt values are different for this event.")

#     print("---")

# Now compare the photon pt values event-by-event
for i, (pts1, pts2) in enumerate(zip(photon_pts_file1, photon_pts_file2)):
    if pts1 != pts2:
        print("Non-identical values found in event {}".format(i+1))
        print("Photon pt values from file 1: {}".format(pts1))
        print("Photon pt values from file 2: {}".format(pts2))
        print("---")
