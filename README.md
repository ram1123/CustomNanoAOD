# Setup

<!-- ```bash
cmsrel CMSSW_10_6_30
cd CMSSW_10_6_30/src
cmsenv
git cms-addpkg PhysicsTools

# copy `NanoTuples` directory from https://github.com/gqlcms/Customized_NanoAOD inside `PhysicsTools` directory
git clone git@github.com:gqlcms/Customized_NanoAOD.git /tmp/rasharma/Customized_NanoAOD
cp -r /tmp/rasharma/Customized_NanoAOD/NanoTuples PhysicsTools/
./PhysicsTools/NanoTuples/scripts/install_onnxruntime.sh
scram b -j8
``` -->

```bash
cmsrel CMSSW_10_6_30
cd CMSSW_10_6_30/src
cmsenv
git cms-merge-topic -u ram1123:CMSSW_10_6_30_HHWWgg_nanoV9
```

## Get the official nanoAOD production for the UL18 campaign

```bash
cd ${CMSSW_BASE}/src
cmsDriver.py  --python_filename HIG-RunIISummer20UL18NanoAODv9-02546_1_cfg_testv1.py --eventcontent NANOAODSIM --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC  --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL18NanoAODv9-02546_testv1.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --filein "dbs:/GluGluToRadionToHHTo2G2WTo2G4Q_M-1000_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM" --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --mc -n 100
```


# OLD setup

1. Use the script [GetCustomNanoAODSet.sh](GetCustomNanoAODSet.sh) to setup the official nanoAOD production for the UL18 campaign.
    - Above script is obtained from the following sources:
        - nanoAOD prepID: [https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIISummer20UL18NanoAODv9-02546&page=0&shown=127](https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIISummer20UL18NanoAODv9-02546&page=0&shown=127)
            - `.sh` script: [https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/HIG-RunIISummer20UL18NanoAODv9-02546](https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/HIG-RunIISummer20UL18NanoAODv9-02546)


```bash
bash GetCustomNanoAODSet.sh
cd CMSSW_10_6_26/src
cmsenv
# git cms-merge-topic -u gouskos:pnet_ak8_new_collection
# git clone https://github.com/hqucms/NanoTuples.git PhysicsTools/NanoTuples --recursive -b production/sv_tagging
scram b -j8
```

# Test

```bash
# cmsDriver.py test_nanoTuples_mc2018 -n 1000 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --nThreads 1 --era Run2_2018,run2_nanoAOD_106Xv2 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein /store/mc/RunIISummer20UL18MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/00000/004EF875-ACBB-FE45-B86B-EAF83448CE62.root --fileout file:nano_mc2018.root --customise_commands "process.options.wantSummary = cms.untracked.bool(True)" >& test_mc2018.log &

# cmsDriver.py  --python_filename HIG-RunIISummer20UL18NanoAODv9-02546_1_cfg_testv1.py --eventcontent NANOAODSIM --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL18NanoAODv9-02546_testv1.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --filein "dbs:/GluGluToRadionToHHTo2G2WTo2G4Q_M-1000_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM" --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --mc -n $EVENTS || exit $? ;

cmsDriver.py test_nanoTuples_mc2018 -n 100 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --nThreads 1 --era Run2_2018,run2_nanoAOD_106Xv2 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC  --filein "dbs:/GluGluToRadionToHHTo2G2WTo2G4Q_M-1000_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM" --fileout file:nano_mc2018.root --customise_commands "process.options.wantSummary = cms.untracked.bool(True)" >& test_mc2018.log &

cmsDriver.py  --python_filename HIG-RunIISummer20UL18NanoAODv9-02546_1_cfg_testv1.py --eventcontent NANOAODSIM --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC  --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL18NanoAODv9-02546_testv1.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --filein "dbs:/GluGluToRadionToHHTo2G2WTo2G4Q_M-1000_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM" --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --mc -n 100


cmsDriver.py  --python_filename HIG-RunIISummer20UL18NanoAODv9-02546_1_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL18NanoAODv9-02546.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --filein "dbs:/GluGluToRadionToHHTo2G2WTo2G4Q_M-1000_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM" --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --mc -n 1000

# less +F test_mc2018.log
```

