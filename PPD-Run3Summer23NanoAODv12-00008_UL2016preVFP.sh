#!/bin/bash

# Binds for singularity containers
# Mount /afs, /eos, /cvmfs, /etc/grid-security for xrootd
export APPTAINER_BINDPATH='/afs,/cvmfs,/cvmfs/grid.cern.ch/etc/grid-security:/etc/grid-security,/eos,/etc/pki/ca-trust,/run/user,/var/run/user'

#############################################################
#   This script is used by McM when it performs automatic   #
#  validation in HTCondor or submits requests to computing  #
#                                                           #
#      !!! THIS FILE IS NOT MEANT TO BE RUN BY YOU !!!      #
# If you want to run validation script yourself you need to #
#     get a "Get test" script which can be retrieved by     #
#  clicking a button next to one you just clicked. It will  #
# say "Get test command" when you hover your mouse over it  #
#      If you try to run this, you will have a bad time     #
#############################################################

# cd /afs/cern.ch/cms/PPD/PdmV/work/McM/submit/PPD-Run3Summer23NanoAODv12-00008/

# Make voms proxy
#voms-proxy-init --voms cms --out $(pwd)/voms_proxy.txt --hours 4
#export X509_USER_PROXY=$(pwd)/voms_proxy.txt


# Dump actual test code to a PPD-Run3Summer23NanoAODv12-00008_UL2016preVFP_test.sh file that can be run in Singularity
cat <<'EndOfTestFile' > PPD-Run3Summer23NanoAODv12-00008_UL2016preVFP_test.sh
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
EVENTS=1000


# cmsDriver command
cmsDriver.py  --python_filename PPD-RunIISummer20UL16preVFP_NanoAODv12-00008_1_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:PPD-Run3Summer23NanoAODv12-00008.root --conditions 106X_mcRun2_asymptotic_preVFP_v11 --step NANO --scenario pp --filein "dbs:/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM" --era Run2_2016_HIPM,run2_nanoAOD_106Xv2 --no_exec --mc -n $EVENTS || exit $? ;

# End of PPD-Run3Summer23NanoAODv12-00008_UL2016preVFP_test.sh file
EndOfTestFile

# Make file executable
chmod +x PPD-Run3Summer23NanoAODv12-00008_UL2016preVFP_test.sh

if [ -e "/cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/el8:amd64" ]; then
  CONTAINER_NAME="el8:amd64"
elif [ -e "/cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/el8:x86_64" ]; then
  CONTAINER_NAME="el8:x86_64"
else
  echo "Could not find amd64 or x86_64 for el8"
  exit 1
fi
export SINGULARITY_CACHEDIR="/tmp/$(whoami)/singularity"
singularity run --no-home /cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/$CONTAINER_NAME $(echo $(pwd)/PPD-Run3Summer23NanoAODv12-00008_UL2016preVFP_test.sh)
