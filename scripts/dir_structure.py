import os

def list_directories(startpath):
    """
    Generate the directory hierarchy for a given path in a string format.
    """
    hierarchy = ""
    for root, dirs, files in os.walk(startpath):
        # print(root, dirs, files)
        # skip following directories: CMSSW_10_6_26, CMSSW_10_6_30, nanoAODv11, __pycache__, logs
        if 'CMSSW_10_6_26' in root or 'CMSSW_10_6_30' in root or 'nanoAODv11' in root or '__pycache__' in root or 'logs' in root or ".git" in root or 'HH_WWgg_Signal_M1000' in root or 'HH_WWgg_Signal_v2' in root:
            continue
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        hierarchy += f"{indent}{os.path.basename(root)}/\n"
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            hierarchy += f"{subindent}{f}\n"
    return hierarchy



# list_directories('/afs/cern.ch/user/r/rasharma/work/doubleHiggs/CustomNanoAOD')
print(list_directories('/afs/cern.ch/user/r/rasharma/work/doubleHiggs/CustomNanoAOD'))
