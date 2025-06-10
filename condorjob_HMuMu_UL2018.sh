#!/bin/bash
# Prevent XALT from interfering with GLIBC
unset LD_PRELOAD
unset XALT_EXECUTABLE_TRACKING
unset XALT_RUN_NOXALT
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

echo "###################################################"

# Step -1: Note the adler32 checksum of the input file from the DAS
echo "------------------------------------------------"
echo "adler32 checksum value from dasgoclient"
dasgoclient --query="file=${InputMiniAODFile}" --json
echo "------------------------------------------------"



echo "Copy the input file to the local directory"
xcacheCopyCommand="xrdcp -f --retry 3 root://xcache.cms.rcac.purdue.edu/${InputMiniAODFile} /dev/null"
globalCopyCommand="xrdcp -f --retry 3 root://cms-xrd-global.cern.ch/${InputMiniAODFile} /dev/null"
fnalCopyCommand="xrdcp -f --retry 3  root://cmsxrootd.fnal.gov/${InputMiniAODFile} /dev/null"

# Print the copy commands
echo "XCache copy command: ${xcacheCopyCommand}"
echo "Global copy command: ${globalCopyCommand}"
echo "FNAL copy command: ${fnalCopyCommand}"

# Step -2: Check the adler32 checksum of the input file
echo "------------------------------------------------"
echo "adler32 checksum value direcoty from /store file"
echo "From xcache: (Used by the code)"
xrdadler32 root://xcache.cms.rcac.purdue.edu/${InputMiniAODFile}
# echo "From global: (As cross-check)"
# xrdadler32 root://cms-xrd-global.cern.ch/${InputMiniAODFile}
# echo "From FNAL: (As cross-check)"
# xrdadler32 root://cmsxrootd.fnal.gov/${InputMiniAODFile}
echo "------------------------------------------------"

# Retry logic for xrdcp command if it fails
# if [ $exitStatus -ne 0 ]; then
#     echo "xrdcp failed, trying again..."
#     xrdcp -f root://xcache.cms.rcac.purdue.edu/${InputMiniAODFile} /dev/null
#     if [ $? -ne 0 ]; then
#         echo "xrdcp failed again, retrying..."
#         xrdcp -f root://xcache.cms.rcac.purdue.edu/${InputMiniAODFile} /dev/null
#         if [ $? -ne 0 ]; then
#           echo "xrdcp failed multiple times, exiting job"
#           exit 1
#         fi
#     fi
# fi

# add xcache redirector to the input file
InputMiniAODFile=root://xcache.cms.rcac.purdue.edu/${InputMiniAODFile}
# InputMiniAODFile=root://cms-xrd-global.cern.ch/${InputMiniAODFile}
echo "Input MiniAOD file after adding xcache redirector: ${InputMiniAODFile}"

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

echo "Input MiniAOD file  before singularity: ${InputMiniAODFile}"
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
  echo 'Executing xcache copy command...'
  echo 'xcacheCopyCommand: ${xcacheCopyCommand}'
  ${xcacheCopyCommand}
  exitStatus=$?
  echo 'Exit status of copy command: ${exitStatus}'
  if [ $exitStatus -ne 0 ]; then
    echo 'xrdcp failed inside Singularity. Exiting.'
    exit 1
  fi
  echo 'Running cmsRun for the given config file'
  echo cmsRun HMuMu/${ConfigFile} inputFiles=file:${InputMiniAODFile} outputFile=///tmp/${OutputNanoAODFile} maxEvents=${maxEvents}
  cmsRun HMuMu/${ConfigFile} inputFiles=file:${InputMiniAODFile} outputFile=///tmp/${OutputNanoAODFile} maxEvents=${maxEvents}
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
    echo "xrdcp -f /tmp/${OutputNanoAODFile} ${OutputDir}/${OutputNanoAODFile}"
    xrdcp -f /tmp/${OutputNanoAODFile} ${OutputDir}/${OutputNanoAODFile}
    echo "Checksum after transfer:"
    xrdadler32 ${OutputDir}/${OutputNanoAODFile}
else
    echo "NanoAOD file not created. Checking for variations..."
    OutputNanoAODfile_noext=${OutputNanoAODFile%.root}
    echo "Checksum before transfer:"
    xrdadler32 /tmp/${OutputNanoAODfile_noext}
    if ls /tmp/${OutputNanoAODfile_noext}*.root 1> /dev/null 2>&1; then
        echo "xrdcp -f /tmp/${OutputNanoAODfile_noext}*.root ${OutputDir}/${OutputNanoAODFile}"
        xrdcp -f /tmp/${OutputNanoAODfile_noext}*.root ${OutputDir}/${OutputNanoAODFile}
        echo "=== checksum after transfer ==="
        xrdadler32 ${OutputDir}/${OutputNanoAODFile}
    else
        echo "Error: ${OutputNanoAODFile} not found."
    fi
fi

# Clean up temporary files
# echo "Deleting the output file from the /tmp directory"
# rm -f /tmp/${OutputNanoAODFile}
# rm -f /tmp/${OutputNanoAODfile_noext}*.root

echo "Job finished at $(date)"
