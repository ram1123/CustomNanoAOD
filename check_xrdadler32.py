file_list_2018 = [
    "root://xcache.cms.rcac.purdue.edu//store/data/Run2018C/SingleMuon/MINIAOD/UL2018_MiniAODv2-v2/70000/CEEEE363-C321-4E43-94D1-96986A919306.root",
    "root://xcache.cms.rcac.purdue.edu//store/data/Run2018C/SingleMuon/MINIAOD/UL2018_MiniAODv2-v2/70000/8965DFA6-19B8-4541-BC7E-650D7A93F3A0.root",
    "root://xcache.cms.rcac.purdue.edu//store/data/Run2018C/SingleMuon/MINIAOD/UL2018_MiniAODv2-v2/70000/C95BEE6E-812F-3242-AE99-60C4E14F2270.root",
    "root://xcache.cms.rcac.purdue.edu//store/data/Run2018C/SingleMuon/MINIAOD/UL2018_MiniAODv2-v2/70000/7B7AD37D-9B94-C249-94AF-FB71A51A216C.root",
    "root://xcache.cms.rcac.purdue.edu//store/data/Run2018C/SingleMuon/MINIAOD/UL2018_MiniAODv2-v2/70000/9CDCB972-BD65-3644-A11E-6D12908B238F.root",
    "root://xcache.cms.rcac.purdue.edu//store/data/Run2018C/SingleMuon/MINIAOD/UL2018_MiniAODv2-v2/70000/F42E368A-1A60-3A4C-BE83-F0F7D6D33D38.root",
    "root://xcache.cms.rcac.purdue.edu//store/data/Run2018C/SingleMuon/MINIAOD/UL2018_MiniAODv2-v2/70000/9D4C6D38-8C31-DC41-AD73-76CC71066316.root",
    "root://xcache.cms.rcac.purdue.edu//store/data/Run2018C/SingleMuon/MINIAOD/UL2018_MiniAODv2-v2/70000/DDED7770-B541-9145-BA26-C8E43264906A.root",
    "root://xcache.cms.rcac.purdue.edu//store/data/Run2018C/SingleMuon/MINIAOD/UL2018_MiniAODv2-v2/70000/08E1DCCA-6F6B-5A41-89AC-D8CC22207EA7.root",
    "root://xcache.cms.rcac.purdue.edu//store/data/Run2018C/SingleMuon/MINIAOD/UL2018_MiniAODv2-v2/70000/C7B0B531-40B4-1640-B89D-0473C5D86142.root"
]

import os

for file in file_list:
    command = f"xrdadler32 {file}"
    # os.system(command)
    result = os.popen(command).read()

    # Print the result
    print(f"Checksum for {file}: {result.strip()}")
