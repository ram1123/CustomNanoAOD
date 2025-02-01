#!/bin/bash

echo "Job started..."
echo "Starting job on " `date`
echo "Running on: `uname -a`"
echo "System software: `cat /etc/redhat-release`"
source /cvmfs/cms.cern.ch/cmsset_default.sh
echo "###################################################"
echo "#    List of Input Arguments: "
echo "###################################################"
echo "Input Arguments (Cluster ID): $1"
echo "Input Arguments (Proc ID): $2"
echo "Input Arguments (Input MiniAOD File): $3"
echo "Input Arguments (Output Directory): $4"

echo "i am here ${PWD}"
basePath=${PWD}

InputMiniAODFile=${3}
OutputNanoAODFile=$(basename $InputMiniAODFile)
outDir=${5}
maxEvents=-1

export APPTAINER_BINDPATH='/afs,/cvmfs,/cvmfs/grid.cern.ch/etc/grid-security:/etc/grid-security,/eos,/etc/pki/ca-trust,/run/user,/var/run/user'

if [ -e "/cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/el8:amd64" ]; then
  CONTAINER_NAME="el8:amd64"
elif [ -e "/cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/el8:x86_64" ]; then
  CONTAINER_NAME="el8:x86_64"
else
  echo "Could not find amd64 or x86_64 for el8"
  exit 1
fi

export SINGULARITY_CACHEDIR="/tmp/$(whoami)/singularity"

singularity exec --no-home /cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/$CONTAINER_NAME /bin/bash -c "
  export SCRAM_ARCH=el8_amd64_gcc11
  source /cvmfs/cms.cern.ch/cmsset_default.sh
  cd CMSSW_13_0_14/src
  eval \`scram runtime -sh\`
  cd ../..

  # Run the Python configuration file
  cmsRun PPD-Run3Summer23NanoAODv12-00008_1_cfg.py inputFiles=${InputMiniAODFile} outputFile=${OutputNanoAODFile} maxEvents=${maxEvents}
"

echo "Job is finished on " `date`
echo "###################################################"

echo "list all the files in the current directory"
ls -ltr
echo "###################################################"

# Check if outDir exists? if not create it
[ ! -d "${outDir}" ] && mkdir -p "${outDir}"
# echo "List all the files in the output directory: ${outDir}"
ls -ltr ${outDir}
echo "###################################################"

# check if the output file is created then copy else give error
if [ -f ${OutputNanoAODFile} ]; then
    echo "xrdcp ${OutputNanoAODFile} ${outDir}/${OutputNanoAODFile}"
    xrdcp ${OutputNanoAODFile} ${outDir}/${OutputNanoAODFile}
else
    OutputNanoAODfile=${OutputNanoAODFile%.root}
    if [ -f ${OutputNanoAODfile}*.root ]; then
        echo "xrdcp ${OutputNanoAODfile}*.root ${outDir}/${OutputNanoAODFile}"
        xrdcp ${OutputNanoAODfile}*.root ${outDir}/${OutputNanoAODFile}
    else
        echo "Error: ${OutputNanoAODFile} is not created"
        echo "list all the files in the current directory"
        ls -ltr
    fi
fi

echo "Ending job on " `date`
