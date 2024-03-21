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
cp -r /tmp/rasharma/Customized_NanoAOD/PhysicsTools/NanoTuples PhysicsTools/
./PhysicsTools/NanoTuples/scripts/install_onnxruntime.sh
scram b -j8

# To get cmssw configuration file
cmsDriver.py  --python_filename HIG-RunIISummer20UL18NanoAODv9-02546_1_cfg.py --eventcontent NANOAODSIM --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC  --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL18NanoAODv9-02546.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --filein "dbs:/GluGluToRadionToHHTo2G2WTo2G4Q_M-1000_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM" --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --mc -n 100
```

## Get cmssw configuration files for MC nanoAOD production

To get the cmssw configuration file for the nanoAOD production, we use the scripts present at mccm for the one of HHWWgg samples.

1. UL18: Ref: https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIISummer20UL18NanoAODv9-02546&page=0&shown=127

    ```bash
    # Command for generating cmssw configuration file For MC, to get nanoAOD from miniAOD file
    cmsDriver.py  --python_filename HIG-RunIISummer20UL18NanoAODv9-02546_1_cfg.py --eventcontent NANOAODSIM --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC  --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL18NanoAODv9-02546.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --filein "dbs:/GluGluToRadionToHHTo2G2WTo2G4Q_M-1000_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM" --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --mc -n 100

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

## Get cmssw configuration files for DATA nanoAOD production

Changes that should be done to get config file for data in MC `cmsDriver.py` commands:

1. Replace `--mc` flag with `--data` flag
2. Replace `--eventcontent NANOAODSIM` with `--eventcontent NANOAOD`
3. Replace `--datatier NANOAODSIM` with `--datatier NANOAOD`
4. Update the "global tag (GT)": Reference pdmv: [https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun2LegacyAnalysis](https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun2LegacyAnalysis)
    - For 2018: `--conditions 106X_upgrade2018_realistic_v16_L1v1` with `--conditions 106X_dataRun2_v37`
    - For 2017: `--conditions 106X_mc2017_realistic_v9` with `--conditions 106X_dataRun2_v37` # INFO: GT for 2017 MC does not match with MCCM and pdmv webpage
    - For 2016: `--conditions 106X_mcRun2_asymptotic_v17` with `--conditions 106X_dataRun2_v37`
    - For 2016APV: `--conditions 106X_mcRun2_asymptotic_preVFP_v11` with `--conditions 106X_dataRun2_v37`
5. Also, need to update the customise function to use the one from nanoTuples_cff.py
    - `--customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData`

### cmsDriver.py commands for DATA nanoAOD production, based on the above changes

1. UL18:

    ```bash
    # Update the customise function to use the one from nanoTuples_cff.py
    cmsDriver.py  --python_filename DATA-Run2018-NanoAODv9-02546_1_cfg.py --eventcontent NANOAOD --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData  --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAOD --fileout file:DATA-Run2018-NanoAODv9-02546.root --conditions 106X_dataRun2_v37 --step NANO --filein "/store/data/Run2018D/EGamma/MINIAOD/UL2018_MiniAODv2-v2/280002/89F5F63C-8F5E-0744-8C0D-73411CC7FE39.root" --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --data -n 100
    ```

1. UL17:

    ```bash
    cmsDriver.py --python_filename DATA-Run2017-NanoAODv9-02407_1_cfg.py --eventcontent NANOAOD --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAOD --fileout file:DATA-Run2017-NanoAODv9-02407.root --conditions 106X_dataRun2_v37 --step NANO --filein "/store/data/Run2017F/EGamma/MINIAOD/UL2017_MiniAODv2-v1/280000/FFA0B0A0-0B5C-5C4A-9B1B-9F6F6B9B9B9B.root" --era Run2_2017,run2_nanoAOD_106Xv2 --no_exec --data -n 100
    ```

1. UL16APV:

    ```bash
    cmsDriver.py --python_filename DATA-Run2016APV-NanoAODv9-01726_1_cfg.py --eventcontent NANOAOD --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAOD --fileout file:DATA-Run2016APV-NanoAODv9-01726.root --conditions 106X_dataRun2_v37 --step NANO --filein "/store/data/Run2016H/EGamma/MINIAOD/UL2016_MiniAODv2-v1/280000/FFA0B0A0-0B5C-5C4A-9B1B-9F6F6B9B9B9B.root" --era Run2_2016_HIPM,run2_nanoAOD_106Xv2 --no_exec --data -n 100
    ```

1. UL16:

    ```bash
    cmsDriver.py --python_filename DATA-Run2016-NanoAODv9-02412_1_cfg.py --eventcontent NANOAOD --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAOD --fileout file:DATA-Run2016-NanoAODv9-02412.root --conditions 106X_dataRun2_v37 --step NANO --filein "/store/data/Run2016H/EGamma/MINIAOD/UL2016_MiniAODv2-v1/280000/FFA0B0A0-0B5C-5C4A-9B1B-9F6F6B9B9B9B.root" --era Run2_2016,run2_nanoAOD_106Xv2 --no_exec --data -n 100
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

4. Add the message logger to print the log file every 10k events not for each event. By default it prints for each event. This increase the log file size. To avoid this, add the following line to the config file:

    ```python
    # Print log file every 10k events
    process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(10000)
    ```
