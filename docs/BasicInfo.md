# nanoAOD production

1. Use the script [GetCustomNanoAODSet.sh](GetCustomNanoAODSet.sh) to setup the official nanoAOD production for the UL18 campaign.
    - Above script is obtained from the following sources:
        - nanoAOD prepID: [https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIISummer20UL18NanoAODv9-02546&page=0&shown=127](https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIISummer20UL18NanoAODv9-02546&page=0&shown=127)
            - `.sh` script: [https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/HIG-RunIISummer20UL18NanoAODv9-02546](https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/HIG-RunIISummer20UL18NanoAODv9-02546)


```bash
cmsrel CMSSW_10_6_30
cd CMSSW_10_6_30/src
cmsenv
git cms-addpkg PhysicsTools
# copy `NanoTuples` directory from https://github.com/gqlcms/Customized_NanoAOD inside `PhysicsTools` directory
git clone git@github.com:gqlcms/Customized_NanoAOD.git /tmp/rasharma/Customized_NanoAOD
cp -r /tmp/rasharma/Customized_NanoAOD/NanoTuples PhysicsTools/
./PhysicsTools/NanoTuples/scripts/install_onnxruntime.sh
scram b -j8

# To get cmssw configuration file
cmsDriver.py  --python_filename HIG-RunIISummer20UL18NanoAODv9-02546_1_cfg.py --eventcontent NANOAODSIM --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC  --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL18NanoAODv9-02546.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --filein "dbs:/GluGluToRadionToHHTo2G2WTo2G4Q_M-1000_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM" --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --mc -n 100
```

## Get cmssw configuration files for nanoAOD production

To get the cmssw configuration file for the nanoAOD production, we use the scripts present at mccm for the one of HHWWgg samples.

1. UL18: Ref: https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIISummer20UL18NanoAODv9-02546&page=0&shown=127

    ```bash
    cmsDriver.py  --python_filename HIG-RunIISummer20UL18NanoAODv9-02546_1_cfg.py --eventcontent NANOAODSIM --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC  --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL18NanoAODv9-02546.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --filein "dbs:/GluGluToRadionToHHTo2G2WTo2G4Q_M-1000_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM" --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --mc -n 100
    ```

2. UL17: Ref: https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIISummer20UL17NanoAODv9-02407&page=0&shown=127

    ```bash
    cmsDriver.py  --python_filename HIG-RunIISummer20UL17NanoAODv9-02407_1_cfg.py --eventcontent NANOAODSIM --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL17NanoAODv9-02407.root --conditions 106X_mc2017_realistic_v9 --step NANO --filein "dbs:/GluGluToRadionToHHTo2G2WTo2G4Q_M-1000_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM" --era Run2_2017,run2_nanoAOD_106Xv2 --no_exec --mc -n 100
    ```
3. UL16APV: Ref: https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIISummer20UL16NanoAODAPVv9-01726&page=0&shown=127

    ```bash
    cmsDriver.py  --python_filename HIG-RunIISummer20UL16NanoAODAPVv9-01726_1_cfg.py --eventcontent NANOAODSIM --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL16NanoAODAPVv9-01726.root --conditions 106X_mcRun2_asymptotic_preVFP_v11 --step NANO --filein "dbs:/GluGluToRadionToHHTo2G2WTo2G4Q_M-1000_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM" --era Run2_2016_HIPM,run2_nanoAOD_106Xv2 --no_exec --mc -n   110
    ```

4. UL16: Ref: https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIISummer20UL16NanoAODv9-02412&page=0&shown=127

    ```bash
    cmsDriver.py  --python_filename HIG-RunIISummer20UL16NanoAODv9-02412_1_cfg.py --eventcontent NANOAODSIM --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL16NanoAODv9-02412.root --conditions 106X_mcRun2_asymptotic_v17 --step NANO --filein "dbs:/GluGluToRadionToHHTo2G2WTo2G4Q_M-1000_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM" --era Run2_2016,run2_nanoAOD_106Xv2 --no_exec --mc -n 110 ;
    ```

## Add input arguments to the cmssw config file

Reference: https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCommandLineParsing#Default_options

```python
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')
options.parseArguments()
```

default options with `VarParsing` that we can use:

```
    maxEvents
    totalSections
    section
    inputFiles
    outputFile
```

Remove the hardcoded input file and number of events from the config file and replace them with the following:

1. For number of events:

    ```python
    process.maxEvents = cms.untracked.PSet(
        input = cms.untracked.int32(options.nEvents)
    )
    ```

2. For input file:

    ```python
    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(options.inputFile)
        secondaryFileNames = cms.untracked.vstring()
    )
    ```

3. For output file:

    ```python
    fileName = cms.untracked.string('file:'+options.outputFile),
    ```
