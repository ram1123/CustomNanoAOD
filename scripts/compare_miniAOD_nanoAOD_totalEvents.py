from __future__ import print_function  # Makes print() function compatible with Python 2 and 3
import sys
import ROOT
import subprocess

# Get two inputs
if len(sys.argv) != 3:
    print("Usage: python compare_miniAOD_nanoAOD_totalEvents.py miniAOD.root nanoAOD.root")
    sys.exit(1)

inputMiniAOD = sys.argv[1]
outputNanoAOD = sys.argv[2]

# ----------------- MiniAOD -----------------
# fullPath_miniAOD = "root://cms-xrd-global.cern.ch/" + inputMiniAOD
fullPath_miniAOD = inputMiniAOD
print("MiniAOD: ", fullPath_miniAOD)

# Open the MiniAOD file using ROOT and get the number of entries in the 'Events' tree
root_file_miniAOD = ROOT.TFile.Open(fullPath_miniAOD)
if not root_file_miniAOD:
    print("Failed to open MiniAOD file.")
    sys.exit(1)

tree_miniAOD = root_file_miniAOD.Get("Events")
if not tree_miniAOD:
    print("Failed to find 'Events' tree in MiniAOD file.")
    sys.exit(1)

nEvents_miniAOD = tree_miniAOD.GetEntries()
print("MiniAOD events: ", nEvents_miniAOD)

# ----------------- NanoAOD -----------------
# outputNanoAOD = outputNanoDirectory + "/" + (inputMiniAOD.split('/')[-1]).replace(".root", "_NanoAOD.root")
outputNanoAOD = outputNanoAOD
print("NanoAOD: ", outputNanoAOD)
# Check if NanoAOD file exists using gfal-ls
try:
    # Execute the gfal-ls command
    result = subprocess.check_call(['gfal-ls', outputNanoAOD], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("NanoAOD file exists.")
except subprocess.CalledProcessError as e:
    # If an error is raised, it means gfal-ls could not find the file or could not access the path
    print("File does not exist or cannot be accessed.")
    print("Error:", e.stderr.decode())
    sys.exit(1)

# Open the NanoAOD file using ROOT and get the number of entries in the 'Events' tree
root_file_nanoAOD = ROOT.TFile.Open(outputNanoAOD)
if not root_file_nanoAOD:
    print("Failed to open NanoAOD file.")
    sys.exit(1)

tree_nanoAOD = root_file_nanoAOD.Get("Events")
if not tree_nanoAOD:
    print("Failed to find 'Events' tree in NanoAOD file.")
    sys.exit(1)

nEvents_nanoAOD = tree_nanoAOD.GetEntries()
print("NanoAOD events: ", nEvents_nanoAOD)

# ----------------- Compare -----------------
if nEvents_miniAOD == nEvents_nanoAOD:
    print("Total events are the same in MiniAOD and NanoAOD.")
else:
    print("Total events are different in MiniAOD and NanoAOD: (mini, nano) = (", nEvents_miniAOD, ", ", nEvents_nanoAOD, ")")
    sys.exit(1)
