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
./PhysicsTools/NanoTuples/scripts/install_onnxruntime.sh
scramv1 b -j 8
cd $CMSSW_BASE/../
```

## Run custom nanoAOD production

```bash
voms-proxy-init --voms cms --valid 168:00

cd ${CMSSW_BASE}/src
cmsenv
cd ../../

# For 2018
cmsRun modified_config_files/HIG-RunIISummer20UL18NanoAODv9-02546_1_cfg.py

# For 2017
cmsRun modified_config_files/HIG-RunIISummer20UL17NanoAODv9-02407_1_cfg.py

# For 2016APV
cmsRun modified_config_files/HIG-RunIISummer20UL16NanoAODAPVv9-01726_1_cfg.py

# For 2016
cmsRun modified_config_files/HIG-RunIISummer20UL16NanoAODv9-02412_1_cfg.py
```

INFO: Use  following command to run the config file with specific root file and number of events.

```bash
cmsRun modified_config_files/HIG-RunIISummer20UL18NanoAODv9-02546_1_cfg.py maxEvents=-1 inputFiles=/store/mc/RunIISummer20UL18MiniAODv2/GluGluToRadionToHHTo2G2WTo2G4Q_M-1000_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/50000/04D3FBF0-A539-5143-9A1C-8D42A1D54C88.root  outputFile=HIG-RunIISummer20UL18NanoAODv9-02546.root
```

## Condor jobs instruction

To create the condor jobs submission script use the script [condor_setup.py](condor_setup.py). This script uses YAML file having list of samples.

```bash
python condor_setup.py --help
```

# Details

## Get the official nanoAOD production config files


```bash
cd ${CMSSW_BASE}/src
cmsenv
cd -

voms-proxy-init --voms cms --valid 168:00

# UL18: Ref: https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIISummer20UL18NanoAODv9-02546&page=0&shown=127
cmsDriver.py  --python_filename HIG-RunIISummer20UL18NanoAODv9-02546_1_cfg.py --eventcontent NANOAODSIM --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC  --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL18NanoAODv9-02546.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --filein "dbs:/GluGluToRadionToHHTo2G2WTo2G4Q_M-1000_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM" --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --mc -n 100

# UL17: Ref: https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIISummer20UL17NanoAODv9-02407&page=0&shown=127
cmsDriver.py  --python_filename HIG-RunIISummer20UL17NanoAODv9-02407_1_cfg.py --eventcontent NANOAODSIM --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL17NanoAODv9-02407.root --conditions 106X_mc2017_realistic_v9 --step NANO --filein "dbs:/GluGluToRadionToHHTo2G2WTo2G4Q_M-1000_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM" --era Run2_2017,run2_nanoAOD_106Xv2 --no_exec --mc -n 100

# UL16APV: Ref: https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIISummer20UL16NanoAODAPVv9-01726&page=0&shown=127
cmsDriver.py  --python_filename HIG-RunIISummer20UL16NanoAODAPVv9-01726_1_cfg.py --eventcontent NANOAODSIM --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL16NanoAODAPVv9-01726.root --conditions 106X_mcRun2_asymptotic_preVFP_v11 --step NANO --filein "dbs:/GluGluToRadionToHHTo2G2WTo2G4Q_M-1000_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM" --era Run2_2016_HIPM,run2_nanoAOD_106Xv2 --no_exec --mc -n 110 ;

# UL16: Ref: https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIISummer20UL16NanoAODv9-02412&page=0&shown=127
cmsDriver.py  --python_filename HIG-RunIISummer20UL16NanoAODv9-02412_1_cfg.py --eventcontent NANOAODSIM --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL16NanoAODv9-02412.root --conditions 106X_mcRun2_asymptotic_v17 --step NANO --filein "dbs:/GluGluToRadionToHHTo2G2WTo2G4Q_M-1000_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM" --era Run2_2016,run2_nanoAOD_106Xv2 --no_exec --mc -n 110 ;
```

## Add input arguments to the cmssw config file

```python
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')
options.parseArguments()
```
Reference: https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCommandLineParsing#Default_options

default options that we can use:

```
    maxEvents
    totalSections
    section
    inputFiles
    outputFile
```

Remove the hardcoded input file and number of events from the config file and replace them with the following:

```python
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.nEvents)
)
```

and

```python
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(options.inputFile)
    secondaryFileNames = cms.untracked.vstring()
)
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

# cmsDriver.py  --python_filename HIG-RunIISummer20UL18NanoAODv9-02546_1_cfg_testv1.py --eventcontent NANOAODSIM --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL18NanoAODv9-02546_testv1.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --filein "dbs:/GluGluToRadionToHHTo2G2WTo2G4Q_M-1000_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM" --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --mc -n 110 ;

cmsDriver.py test_nanoTuples_mc2018 -n 100 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --nThreads 1 --era Run2_2018,run2_nanoAOD_106Xv2 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC  --filein "dbs:/GluGluToRadionToHHTo2G2WTo2G4Q_M-1000_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM" --fileout file:nano_mc2018.root --customise_commands "process.options.wantSummary = cms.untracked.bool(True)" >& test_mc2018.log &

cmsDriver.py  --python_filename HIG-RunIISummer20UL18NanoAODv9-02546_1_cfg_testv1.py --eventcontent NANOAODSIM --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC  --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL18NanoAODv9-02546_testv1.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --filein "dbs:/GluGluToRadionToHHTo2G2WTo2G4Q_M-1000_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM" --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --mc -n 100


cmsDriver.py  --python_filename HIG-RunIISummer20UL18NanoAODv9-02546_1_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL18NanoAODv9-02546.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --filein "dbs:/GluGluToRadionToHHTo2G2WTo2G4Q_M-1000_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM" --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --mc -n 1000

# less +F test_mc2018.log
```

