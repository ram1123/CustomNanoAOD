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

mv ../../Configuration .
scram b
cd ../..

# Maximum validation duration: 28800s
# Margin for validation duration: 30%
# Validation duration with margin: 28800 * (1 - 0.30) = 20160s
# Time per event for each sequence: 0.3402s
# Threads for each sequence: 4
# Time per event for single thread for each sequence: 4 * 0.3402s = 1.3608s
# Which adds up to 1.3608s per event
# Single core events that fit in validation duration: 20160s / 1.3608s = 14814
# Produced events limit in McM is 10000
# According to 1.0000 efficiency, validation should run 10000 / 1.0000 = 10000 events to reach the limit of 10000
# Take the minimum of 14814 and 10000, but more than 0 -> 10000
# It is estimated that this validation will produce: 10000 * 1.0000 = 10000 events
EVENTS=10000


# cmsDriver command
cmsDriver.py  --python_filename PPD-Run3Summer23NanoAODv12-00008_1_cfg.py --eventcontent NANOEDMAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:PPD-Run3Summer23NanoAODv12-00008.root --conditions 130X_mcRun3_2023_realistic_v14 --step NANO --scenario pp --filein "dbs:/DYJetsToLL_M-10to50_TuneCP5_13p6TeV-madgraphMLM-pythia8/Run3Winter22MiniAOD-122X_mcRun3_2021_realistic_v9-v2/MINIAODSIM" --era Run3_2023 --no_exec --mc -n $EVENTS || exit $? ;
cmsRun PPD-Run3Summer23NanoAODv12-00008_1_cfg.py
# End of PPD-Run3Summer23NanoAODv12-00008_test.sh file
