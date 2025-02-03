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
cmsDriver.py --python_filename PPD-RunIISummer20UL18_NanoAODv12_data_cfg.py \
  --eventcontent NANOAOD \
  --customise Configuration/DataProcessing/Utils.addMonitoring \
  --datatier NANOAOD \
  --fileout file:PPD-RunIISummer20UL18_NanoAODv12.root \
  --conditions 106X_dataRun2_v37 \
  --step NANO \
  --scenario pp \
  --filein "/store/mc/RunIISummer20UL18MiniAODv2/DYJetsToLL_0J_MLL_1400_2300_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v3/40000/1D68BF65-D234-5F4E-B922-81ADBA88C361.root" \
  --era Run2_2018,run2_nanoAOD_106Xv2 \
  --no_exec --data -n $EVENTS || exit $? ;

# cmsRun PPD-RunIISummer20UL18_NanoAODv12_data_cfg.py

# End of PPD-RunIISummer20UL18_NanoAODv12_test_data.sh file
