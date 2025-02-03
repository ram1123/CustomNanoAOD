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
cmsDriver.py --python_filename PPD-RunIISummer20UL17_NanoAODv12_cfg.py \
  --eventcontent NANOAODSIM \
  --customise Configuration/DataProcessing/Utils.addMonitoring \
  --datatier NANOAODSIM \
  --fileout file:PPD-RunIISummer20UL17_NanoAODv12.root \
  --conditions 106X_mc2017_realistic_v9 \
  --step NANO \
  --scenario pp \
  --filein "/store/mc/RunIISummer20UL17MiniAODv2/DYJetsToLL_0J_MLL_1400_2300_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v3/40000/045834D5-A065-7743-8A8E-EAF03757451C.root" \
  --era Run2_2017,run2_nanoAOD_106Xv2 \
  --no_exec --mc -n $EVENTS || exit $? ;

# cmsRun PPD-RunIISummer20UL17_NanoAODv12_cfg.py

# End of PPD-RunIISummer20UL17_NanoAODv12_test.sh file
