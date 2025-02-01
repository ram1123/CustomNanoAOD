# Add few patches to the python config files

## Add the VarParsing module

```python
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')
options.parseArguments()
```

### Update the following lines

```python
    input = cms.untracked.int32(options.maxEvents),
    fileNames = cms.untracked.vstring(options.inputFiles),
    annotation = cms.untracked.string('--python_filename nevts:'+str(options.maxEvents)),
    fileName = cms.untracked.string('file:'+options.outputFile),
```

## Add the following lines to print the log file every 10k events

```python
# Print log file every 1000 events
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)
```


# Command to run the script

bash RunConfig.sh 11 11 PPD-RunIISummer20UL18_NanoAODv12_cfg.py /store/mc/RunIISummer20UL18MiniAODv2/DYJetsToLL_0J_MLL_1400_2300_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v3/40000/1D68BF65-D234-5F4E-B922-81ADBA88C361.root ram  100
bash RunConfig.sh 11 11 PPD-RunIISummer20UL17_NanoAODv12_cfg.py /store/mc/RunIISummer20UL17MiniAODv2/DYJetsToLL_0J_MLL_1400_2300_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v3/40000/045834D5-A065-7743-8A8E-EAF03757451C.root ram 100
bash RunConfig.sh 11 11 PPD-RunIISummer20UL16postVFP_NanoAODv12_cfg.py /store/mc/RunIISummer20UL16MiniAODv2/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v1/2520000/04A698D5-2AF9-B548-9A6D-DB5AFE92F0A6.root ram 11
bash RunConfig.sh 11 11 PPD-RunIISummer20UL16preVFP_NanoAODv12_cfg.py /store/mc/RunIISummer20UL16MiniAODAPVv2/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/120000/008E4139-6019-CE4C-B83C-A849F56F57B3.root ram 100

