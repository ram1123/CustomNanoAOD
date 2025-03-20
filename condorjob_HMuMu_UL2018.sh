#!/bin/bash

echo "Job started..."
echo "Starting job on $(date)"
echo "Running on: $(uname -a)"
echo "System software: $(cat /etc/redhat-release)"
source /cvmfs/cms.cern.ch/cmsset_default.sh
echo "###################################################"
echo "#    List of Input Arguments: "
echo "###################################################"
echo "Input Arguments (Cluster ID): $1"
echo "Input Arguments (Proc ID): $2"
echo "Input Arguments (Python Config File): $3"
echo "Input Arguments (Input MiniAOD File): $4"
echo "Input Arguments (Output Directory): $5"
echo "Input Arguments (#Events): $6"

# Positional parameters
ClusterID=$1
ProcID=$2
ConfigFile=$3
InputMiniAODFile=$4
OutputDir=$5
maxEvents=$6

# Step -1: Note the adler32 checksum of the input file from the DAS
adler32_value_das=$(dasgoclient --query="file=${InputMiniAODFile}" --json | jq -r '.[0].file[0].adler32')
echo "adler32 checksum value from dasgoclient: ${adler32_value_das}"

# Step -2: Check the adler32 checksum of the input file
adler32_value_store=$(xrdadler32 root://xcache.cms.rcac.purdue.edu/${InputMiniAODFile} | awk '{print $1}')
echo "adler32 checksum value from xrdadler32: ${adler32_value_store}"

# Step -3: Compare the two adler32 checksum values
if [ "$adler32_value_das" == "$adler32_value_store" ]; then
    echo "Checksum values match: ${adler32_value_das} == ${adler32_value_store}"
else
    echo "Checksum values do not match: ${adler32_value_das} != ${adler32_value_store}"
    exit 1
fi

echo "Copy the input file to the local directory"
xcacheCopyCommand="xrdcp -f root://xcache.cms.rcac.purdue.edu/${InputMiniAODFile} /dev/null"
globalCopyCommand="xrdcp -f root://cms-xrd-global.cern.ch/${InputMiniAODFile} /dev/null"
fnalCopyCommand="xrdcp -f root://cmsxrootd.fnal.gov/${InputMiniAODFile} /dev/null"

# Print the copy commands
echo "XCache copy command: ${xcacheCopyCommand}"
echo "Global copy command: ${globalCopyCommand}"
echo "FNAL copy command: ${fnalCopyCommand}"

# Execute the copy command (Choose the appropriate one)
echo "Executing xcache copy command..."
${xcacheCopyCommand}
exitStatus=$?
echo "Exit status of copy command: ${exitStatus}"

# Retry logic for xrdcp command if it fails
if [ $exitStatus -ne 0 ]; then
    echo "xrdcp failed, trying again..."
    xrdcp -f root://xcache.cms.rcac.purdue.edu/${InputMiniAODFile} /dev/null
    if [ $? -ne 0 ]; then
        echo "xrdcp failed again, retrying..."
        xrdcp -f root://xcache.cms.rcac.purdue.edu/${InputMiniAODFile} /dev/null
        if [ $? -ne 0 ]; then
          echo "xrdcp failed multiple times, exiting job"
          exit 1
        fi
    fi
fi

# Determine the output file name from the input file
OutputNanoAODFile=$(basename ${InputMiniAODFile})
OutputNanoAODFile=${OutputNanoAODFile/.root/_NanoAOD.root}  # Replace .root with _NanoAOD.root
echo "Output nanoAOD file: ${OutputNanoAODFile}"

# Setup Singularity binding and container selection
export APPTAINER_BINDPATH='/cvmfs,/cvmfs/grid.cern.ch/etc/grid-security:/etc/grid-security,/etc/pki/ca-trust,/run/user,/var/run/user'

# Determine Singularity container name based on availability
if [ -e "/cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/el8:amd64" ]; then
  CONTAINER_NAME="el8:amd64"
elif [ -e "/cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/el8:x86_64" ]; then
  CONTAINER_NAME="el8:x86_64"
else
  echo "Could not find amd64 or x86_64 for el8 container"
  exit 1
fi

export SINGULARITY_CACHEDIR="/tmp/$(whoami)/singularity"

# Execute the job inside the Singularity container
singularity exec --no-home /cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/$CONTAINER_NAME /bin/bash -c "
  export SCRAM_ARCH=el8_amd64_gcc11
  source /cvmfs/cms.cern.ch/cmsset_default.sh
  if [ -r CMSSW_13_0_14/src ]; then
    echo 'Release CMSSW_13_0_14 already exists'
  else
    scram p CMSSW CMSSW_13_0_14
  fi
  cd CMSSW_13_0_14/src
  eval \`scram runtime -sh\`
  cd ../..
  echo 'Running cmsRun for the given config file'
  echo cmsRun ${ConfigFile} inputFiles=file:${InputMiniAODFile} outputFile=///tmp/${OutputNanoAODFile} maxEvents=${maxEvents}
  cmsRun ${ConfigFile} inputFiles=file:${InputMiniAODFile} outputFile=///tmp/${OutputNanoAODFile} maxEvents=${maxEvents}
  echo "CMSRun finished with exit code: $?"
  echo "------------------------------------------------"
  echo "Comparing MiniAOD and NanoAOD files"
  echo "------------------------------------------------"
  python compare_miniAOD_nanoAOD_totalEvents.py ${InputMiniAODFile} ///tmp/${OutputNanoAODFile}
  echo "------------------------------------------------"
"

# Final steps: checksum verification and file transfer
if [ -f /tmp/${OutputNanoAODFile} ]; then
    echo "Checksum before transfer:"
    xrdadler32 /tmp/${OutputNanoAODFile}

    xrdcp -f /tmp/${OutputNanoAODFile} ${OutputDir}/${OutputNanoAODFile}
    echo "Checksum after transfer:"
    xrdadler32 ${OutputDir}/${OutputNanoAODFile}
else
    echo "NanoAOD file not created. Checking for variations..."
    OutputNanoAODfile_noext=${OutputNanoAODFile%.root}
    xrdadler32 /tmp/${OutputNanoAODfile_noext}
    if ls /tmp/${OutputNanoAODfile_noext}*.root 1> /dev/null 2>&1; then
        xrdcp -f /tmp/${OutputNanoAODfile_noext}*.root ${OutputDir}/${OutputNanoAODFile}
        echo "=== checksum after transfer ==="
        xrdadler32 ${OutputDir}/${OutputNanoAODFile}
    else
        echo "Error: ${OutputNanoAODFile} not found."
    fi
fi

# Clean up temporary files
echo "Deleting the output file from the /tmp directory"
rm -f /tmp/${OutputNanoAODFile}
rm -f /tmp/${OutputNanoAODfile_noext}*.root

echo "Job finished at $(date)"
