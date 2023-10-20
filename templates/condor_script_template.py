sh_file_template = '''#!/bin/bash

echo "{test}"
echo "Starting job on " `date`
echo "Running on: `uname -a`"
echo "System software: `cat /etc/redhat-release`"
source /cvmfs/cms.cern.ch/cmsset_default.sh
echo "###################################################"
echo "#    List of Input Arguments: "
echo "###################################################"
echo "Input Arguments (Cluster ID): $1"
echo "Input Arguments (Proc ID): $2"
echo "Input Arguments (CMSSW Config File): $3"
echo "Input Arguments (Input MiniAOD File): $4"
echo "Input Arguments (Output NanoAOD File): $5"
echo "Input Arguments (Output Directory): $6"

echo "i am here ${{PWD}}"
basePath=${{PWD}}

nanoCMSSW=CMSSW_10_6_30

cmsConfigFile=${{3}}
InputMiniAODFile=${{4}}
OutputNanoAODFile=${{5}}
outDir=${{6}}

export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh

scram p CMSSW ${{nanoCMSSW}}
cd ${{nanoCMSSW}}/src
eval `scram runtime -sh`
git cms-merge-topic -u ram1123:CMSSW_10_6_30_HHWWgg_nanoV9
./PhysicsTools/NanoTuples/scripts/install_onnxruntime.sh
scram b -j 8
cd -
echo "###################################################"
echo "Job is starting on " `date`
echo "cmsRun ${{cmsConfigFile}} inputFiles=${{InputMiniAODFile}} outputFile=${{OutputNanoAODFile}} maxEvents={maxEvents}"
cmsRun ${{cmsConfigFile}} inputFiles=${{InputMiniAODFile}} outputFile=${{OutputNanoAODFile}} maxEvents={maxEvents}
echo "Job is finished on " `date`
echo "###################################################"

echo "list all the files in the current directory"
ls -ltr
echo "###################################################"

# Check if outDir exists? if not create it
[ ! -d "${{outDir}}" ] && mkdir -p "${{outDir}}"
echo "List all the files in the output directory: ${{outDir}}"
ls -ltr ${{outDir}}
echo "###################################################"

# check if the output file is created then copy else give error
if [ -f ${{OutputNanoAODFile}} ]; then
    echo "cp ${{OutputNanoAODFile}} ${{outDir}}/${{OutputNanoAODFile}}"
    cp ${{OutputNanoAODFile}} ${{outDir}}/${{OutputNanoAODFile}}
else
    OutputNanoAODfile=${{OutputNanoAODFile%.root}}
    if [ -f ${{OutputNanoAODfile}}*.root ]; then
        echo "cp ${{OutputNanoAODfile}}*.root ${{outDir}}/${{OutputNanoAODFile}}"
        cp ${{OutputNanoAODfile}}*.root ${{outDir}}/${{OutputNanoAODFile}}
    else
        echo "Error: ${{OutputNanoAODFile}} is not created"
        echo "list all the files in the current directory"
        ls -ltr
    fi
fi

echo "Ending job on " `date`
'''


jdl_file_template_part1of2 = '''Executable = {CondorExecutable}.sh
Universe = vanilla
Notification = ERROR
Should_Transfer_Files = YES
Transfer_Output_Files = ""
Transfer_Input_Files = {CondorExecutable}.sh, {cmsswConfigFile}
x509userproxy = $ENV(X509_USER_PROXY)
getenv      = True
+JobFlavour = "{CondorQueue}"
request_memory = 12000
request_cpus = 8
'''


jdl_file_template_part2of2 = '''Output = {CondorLogPath}/log_$(Cluster)_$(Process).stdout
Error  = {CondorLogPath}/log_$(Cluster)_$(Process).stdout
Log  = {CondorLogPath}/log_$(Cluster)_$(Process).err
Arguments = $(Cluster) $(Process)   {cmsswConfigFile} {InputMiniAODFile} {OutputNanoAODFile} {outDir}
Queue {queue}
'''
