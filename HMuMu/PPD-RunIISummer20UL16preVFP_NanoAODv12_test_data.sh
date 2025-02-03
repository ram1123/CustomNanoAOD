#!/bin/bash

export SCRAM_ARCH=el8_amd64_gcc11
source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_13_0_14/src ] ; then
  echo release CMSSW_13_0_14 already exists
else
  scram p CMSSW CMSSW_13_0_14
fi
cd CMSSW_13_0_14/src
eval `scram runtime -sh`
# mv ../../Configuration .
scram b
cd ../..

EVENTS=-1

# cmsDriver command with era-specific options:
cmsDriver.py --python_filename PPD-RunIISummer20UL16preVFP_NanoAODv12_data_cfg.py \
  --eventcontent NANOAOD \
  --customise Configuration/DataProcessing/Utils.addMonitoring \
  --datatier NANOAOD \
  --fileout file:PPD-RunIISummer20UL16preVFP_NanoAODv12.root \
  --conditions 106X_dataRun2_v37 \
  --step NANO \
  --scenario pp \
  --filein "/store/mc/RunIISummer20UL16MiniAODAPVv2/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/120000/008E4139-6019-CE4C-B83C-A849F56F57B3.root" \
  --era Run2_2016_HIPM,run2_nanoAOD_106Xv2 \
  --no_exec --data -n $EVENTS || exit $? ;

# cmsRun PPD-RunIISummer20UL16preVFP_NanoAODv12_data_cfg.py

# End of PPD-RunIISummer20UL16preVFP_NanoAODv12_test_data.sh file
