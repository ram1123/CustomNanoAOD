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


echo "Copy the input file to the local directory"
# echo "xrdcp -f   root://cms-xrd-global.cern.ch/${InputMiniAODFile} ${PWD}"
# xrdcp -f root://cms-xrd-global.cern.ch/${InputMiniAODFile} ${PWD}
# echo "xrdcp  root://cmsxrootd.fnal.gov/${InputMiniAODFile} ${PWD}"
echo "xrdcp root://xcache.cms.rcac.purdue.edu/${InputMiniAODFile} ${PWD}"
xrdcp -f  root://xcache.cms.rcac.purdue.edu/${InputMiniAODFile} /dev/null
# $? not zero then try again xrdcp
if [ $? -ne 0 ]; then
    echo "xrdcp failed, try again"
    xrdcp -f  root://xcache.cms.rcac.purdue.edu/${InputMiniAODFile} /dev/null
    if [ $? -ne 0 ]; then
        echo "xrdcp failed again, try again"
        xrdcp -f  root://xcache.cms.rcac.purdue.edu/${InputMiniAODFile} /dev/null
        if [ $? -ne 0 ]; then
          echo "xrdcp failed again, exit"
          exit 1
        fi
    fi
fi

# Update the name of the input file to the local directory
# InputMiniAODFile=$(basename $InputMiniAODFile)
InputMiniAODFile=root://xcache.cms.rcac.purdue.edu/${InputMiniAODFile}
# InputMiniAODFile=root://cms-xrd-global.cern.ch/${InputMiniAODFile}
# InputMiniAODFile=root://cmsxrootd.fnal.gov/${InputMiniAODFile}

echo "i am here ${PWD}"
basePath=${PWD}

# Determine output file name from input file; you might modify this logic as needed.
OutputNanoAODFile=$(basename $InputMiniAODFile)
OutputNanoAODFile=${OutputNanoAODFile/.root/_NanoAOD.root} # Replace .root with _NanoAOD.root
# OutputNanoAODFile=${InputMiniAODFile/.root/_NanoAOD.root} # Replace .root with _NanoAOD.root
# create directory if not exists
# mkdir /tmp/shar1172
# OutputNanoAODFile=/tmp/shar1172/${OutputNanoAODFile}




echo "Output nanoAOD file: ${OutputNanoAODFile}"

# Setup Singularity binding and container selection
export APPTAINER_BINDPATH='/cvmfs,/cvmfs/grid.cern.ch/etc/grid-security:/etc/grid-security,/etc/pki/ca-trust,/run/user,/var/run/user'

if [ -e "/cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/el8:amd64" ]; then
  CONTAINER_NAME="el8:amd64"
elif [ -e "/cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/el8:x86_64" ]; then
  CONTAINER_NAME="el8:x86_64"
else
  echo "Could not find amd64 or x86_64 for el8"
  exit 1
fi

export SINGULARITY_CACHEDIR="/tmp/$(whoami)/singularity"

# Execute the config file inside the container using singularity
singularity exec --no-home /cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/$CONTAINER_NAME /bin/bash -c "
  export SCRAM_ARCH=el8_amd64_gcc11
  source /cvmfs/cms.cern.ch/cmsset_default.sh
  if [ -r CMSSW_13_0_14/src ] ; then
    echo release CMSSW_13_0_14 already exists
  else
    scram p CMSSW CMSSW_13_0_14
  fi
  # ls
  cd CMSSW_13_0_14/src
  pwd
  eval \`scram runtime -sh\`
  cd ../..
  pwd


  # Run the Python configuration file with arguments (if supported by the config)
  echo Running command: cmsRun ${ConfigFile} inputFiles=file:${InputMiniAODFile} outputFile=///tmp/${OutputNanoAODFile} maxEvents=${maxEvents}
  cmsRun ${ConfigFile} inputFiles=file:${InputMiniAODFile} outputFile=///tmp/${OutputNanoAODFile} maxEvents=${maxEvents}
"

echo "Job is finished on " `date`
echo "###################################################"

echo "Listing files in the current directory:"
ls -ltr *.root
echo "Listing files in the /tmp directory:"
ls -ltr /tmp/*.root
echo "###################################################"

# Create output directory if it does not exist
echo "###################################################"

# Check if the output file is created, then copy it; if not, try alternative file name patterns
if [ -f /tmp/${OutputNanoAODFile} ]; then
    echo "=== checksum before trasnfer ==="
    xrdadler32 /tmp/${OutputNanoAODFile}
    echo "=== checksum END ==="
    echo "xrdcp -f -d 2 /tmp/${OutputNanoAODFile} ${OutputDir}/${OutputNanoAODFile}"
    xrdcp -f  /tmp/${OutputNanoAODFile} ${OutputDir}/${OutputNanoAODFile}
    echo "=== checksum after transfer ==="
    xrdadler32 ${OutputDir}/${OutputNanoAODFile}
    echo "=== checksum END ==="
else
    OutputNanoAODfile_noext=${OutputNanoAODFile%.root}
    echo "=== checksum before transfer ==="
    xrdadler32 /tmp/${OutputNanoAODfile_noext}
    echo "=== checksum END ==="
    if ls /tmp/${OutputNanoAODfile_noext}*.root 1> /dev/null 2>&1; then
        echo "xrdcp -f -d 2 /tmp/${OutputNanoAODfile_noext}*.root ${OutputDir}/${OutputNanoAODFile}"
        # xrdcp -f -d 2 /tmp/${OutputNanoAODfile_noext}*.root ${OutputDir}/${OutputNanoAODFile}
        xrdcp -f  /tmp/${OutputNanoAODfile_noext}*.root ${OutputDir}/${OutputNanoAODFile}
        echo "=== checksum after transfer ==="
        xrdadler32 ${OutputDir}/${OutputNanoAODFile}
        echo "=== checksum END ==="
    else
        echo "Error: ${OutputNanoAODFile} is not created"
        echo "Listing files in the current directory:"
        # ls -ltr
    fi
fi

echo "###################################################"
echo "Deleting the output file from the /tmp directory"
rm -f /tmp/${OutputNanoAODFile}
rm -f /tmp/${OutputNanoAODfile_noext}*.root
echo "Listing files in the /tmp directory:"
# ls -ltr /tmp
echo "###################################################"

echo "Ending job on " `date`
