#!/bin/bash

# Binds for singularity containers
export APPTAINER_BINDPATH='/afs,/cvmfs,/cvmfs/grid.cern.ch/etc/grid-security:/etc/grid-security,/eos,/etc/pki/ca-trust,/run/user,/var/run/user'

# Make voms proxy (uncomment if needed)
# voms-proxy-init --voms cms --out $(pwd)/voms_proxy.txt --hours 4
# export X509_USER_PROXY=$(pwd)/voms_proxy.txt

# Dump test code to a file (the name will be replaced)
cat <<'EndOfTestFile' > PPD-RunIISummer20UL16postVFP_NanoAODv12_test.sh
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
cmsDriver.py --python_filename PPD-RunIISummer20UL16postVFP_NanoAODv12_cfg.py \
  --eventcontent NANOAODSIM \
  --customise Configuration/DataProcessing/Utils.addMonitoring \
  --datatier NANOAODSIM \
  --fileout file:PPD-RunIISummer20UL16postVFP_NanoAODv12.root \
  --conditions 106X_mcRun2_asymptotic_v17 \
  --step NANO \
  --scenario pp \
  --filein "/store/mc/RunIISummer20UL16MiniAODv2/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v1/2520000/04A698D5-2AF9-B548-9A6D-DB5AFE92F0A6.root" \
  --era Run2_2016,run2_nanoAOD_106Xv2 \
  --no_exec --mc -n $EVENTS || exit $? ;

# cmsRun PPD-RunIISummer20UL16postVFP_NanoAODv12_cfg.py

# End of PPD-RunIISummer20UL16postVFP_NanoAODv12_test.sh file
EndOfTestFile

chmod +x PPD-RunIISummer20UL16postVFP_NanoAODv12_test.sh

if [ -e "/cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/el8:amd64" ]; then
  CONTAINER_NAME="el8:amd64"
elif [ -e "/cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/el8:x86_64" ]; then
  CONTAINER_NAME="el8:x86_64"
else
  echo "Could not find amd64 or x86_64 for el8"
  exit 1
fi

export SINGULARITY_CACHEDIR="/tmp/$(whoami)/singularity"
singularity run --no-home /cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/$CONTAINER_NAME $(echo $(pwd)/PPD-RunIISummer20UL16postVFP_NanoAODv12_test.sh)
