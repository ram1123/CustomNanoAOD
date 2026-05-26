sh_file_template = r'''#!/bin/bash

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
# echo "List all the files in the output directory: ${{outDir}}"
ls -ltr ${{outDir}}
echo "###################################################"

# check if the output file is created then copy else give error
if [ -f ${{OutputNanoAODFile}} ]; then
    echo "xrdcp ${{OutputNanoAODFile}} ${{outDir}}/${{OutputNanoAODFile}}"
    xrdcp ${{OutputNanoAODFile}} ${{outDir}}/${{OutputNanoAODFile}}
else
    OutputNanoAODfile=${{OutputNanoAODFile%.root}}
    if [ -f ${{OutputNanoAODfile}}*.root ]; then
        echo "xrdcp ${{OutputNanoAODfile}}*.root ${{outDir}}/${{OutputNanoAODFile}}"
        xrdcp ${{OutputNanoAODfile}}*.root ${{outDir}}/${{OutputNanoAODFile}}
    else
        echo "Error: ${{OutputNanoAODFile}} is not created"
        echo "list all the files in the current directory"
        ls -ltr
    fi
fi

echo "Ending job on " `date`
'''

sh_file_template_HMuMu = r"""#!/bin/bash

set -euo pipefail

# Prevent XALT / LD_PRELOAD issues on Gautschi login and worker nodes
unset LD_PRELOAD
unset XALT_EXECUTABLE_TRACKING
unset XALT_RUN_NOXALT

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
echo "Input Arguments (Input MiniAOD Files): $4"
echo "Input Arguments (Output Directory): $5"
echo "Input Arguments (Output File): $6"
echo "Input Arguments (#Events): $7"
echo "Input Arguments (Input Redirector): $8"

# Positional parameters
ClusterID=$1
ProcID=$2
ConfigFile=$3
InputMiniAODFiles=$4
OutputDir=$5
OutputNanoAODFile=$6

# Optional max events; default is -1 (all events)
maxEvents=$7
InputRedirector=$8

echo "i am here ${{PWD}}"
basePath=${{PWD}}

JobWorkDir="/tmp/${{USER}}/custom_nanoaod_${{ClusterID}}_${{ProcID}}"
mkdir -p "${{JobWorkDir}}"
echo "Using isolated job work directory: ${{JobWorkDir}}"
cd "${{JobWorkDir}}"

if [ -f "${{basePath}}/${{ConfigFile}}" ]; then
  ResolvedConfigFile="${{basePath}}/${{ConfigFile}}"
elif [ -f "${{basePath}}/HMuMu/${{ConfigFile}}" ]; then
  ResolvedConfigFile="${{basePath}}/HMuMu/${{ConfigFile}}"
elif [ -f "${{basePath}}/cmssw_modified_config_files/${{ConfigFile}}" ]; then
  ResolvedConfigFile="${{basePath}}/cmssw_modified_config_files/${{ConfigFile}}"
elif [ -f "${{basePath}}/cmssw_default_config_files/${{ConfigFile}}" ]; then
  ResolvedConfigFile="${{basePath}}/cmssw_default_config_files/${{ConfigFile}}"
else
  echo "Error: could not locate config file ${{ConfigFile}}"
  exit 1
fi
echo "Resolved config file: ${{ResolvedConfigFile}}"

IFS=',' read -r -a InputMiniAODArray <<< "${{InputMiniAODFiles}}"
ResolvedInputFiles=()
for file in "${{InputMiniAODArray[@]}}"; do
  if [[ "$file" == root://* ]] || [[ "$file" == file:* ]]; then
    ResolvedInputFiles+=("$file")
  else
    ResolvedInputFiles+=("${{InputRedirector}}${{file}}")
  fi
done

CmsRunInputFiles=$(IFS=,; echo "${{ResolvedInputFiles[*]}}")

export SCRAM_ARCH=el8_amd64_gcc12
export JOB_CMSSW_RELEASE=CMSSW_15_0_15_patch4

echo "Using SCRAM_ARCH=${{SCRAM_ARCH}}"
echo "Using CMSSW release=${{JOB_CMSSW_RELEASE}}"

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r ${{JOB_CMSSW_RELEASE}}/src ] ; then
  echo release ${{JOB_CMSSW_RELEASE}} already exists
else
  scram p CMSSW ${{JOB_CMSSW_RELEASE}}
fi
cd ${{JOB_CMSSW_RELEASE}}/src
eval `scram runtime -sh`

if [ -d "${{basePath}}/Configuration" ] && [ ! -d Configuration ]; then
  cp -r "${{basePath}}/Configuration" .
fi

scram b
cd "${{JobWorkDir}}"
pwd

echo "Running cmsRun ${{ResolvedConfigFile}} inputFiles=${{CmsRunInputFiles}} outputFile=${{OutputNanoAODFile}} maxEvents=${{maxEvents}}"
cmsRun "${{ResolvedConfigFile}}" inputFiles=${{CmsRunInputFiles}} outputFile=${{OutputNanoAODFile}} maxEvents=${{maxEvents}}

echo "cmsRun finished successfully"

ActualOutputFile="${{OutputNanoAODFile}}"
DerivedCfgOutputFile="$(basename "${{ResolvedConfigFile}}")"
DerivedCfgOutputFile="${{DerivedCfgOutputFile%_1_cfg.py}}.root"

if [ ! -f "${{ActualOutputFile}}" ] && [ -f "${{DerivedCfgOutputFile}}" ]; then
  echo "Requested output file was not created directly; using cfg-derived file ${{DerivedCfgOutputFile}}"
  ActualOutputFile="${{DerivedCfgOutputFile}}"
fi

echo "Job is finished on " `date`
echo "###################################################"

echo "Listing files in the current directory:"
ls -ltr
echo "###################################################"

echo "Remote output target: ${{OutputDir}}/${{OutputNanoAODFile}}"
echo "###################################################"

if [[ "${{OutputDir}}" =~ ^root://([^/]+)(/.*)$ ]]; then
    OutputDirHost="root://${{BASH_REMATCH[1]}}"
    OutputDirPath="${{BASH_REMATCH[2]}}"
    RemoteOutputDir="${{OutputDirPath}}"
    echo "Ensuring remote output directory exists: ${{OutputDirHost}} ${{RemoteOutputDir}}"
    if command -v xrdfs >/dev/null 2>&1; then
        if ! xrdfs "${{OutputDirHost}}" mkdir -p "${{RemoteOutputDir}}"; then
            echo "Warning: xrdfs mkdir failed; continuing to xrdcp transfer attempt."
        fi
    else
        echo "Warning: xrdfs is not available on this worker node; continuing to xrdcp transfer attempt."
    fi
fi

# Check if the output file is created, then copy it; if not, try alternative file name patterns
if [ -f "${{ActualOutputFile}}" ]; then
    echo "xrdcp -f ${{ActualOutputFile}} ${{OutputDir}}/${{OutputNanoAODFile}}"
    xrdcp -f "${{ActualOutputFile}}" "${{OutputDir}}/${{OutputNanoAODFile}}"
    echo "Removing local file after successful transfer: ${{ActualOutputFile}}"
    rm -f "${{ActualOutputFile}}"
else
    OutputNanoAODfile_noext=${{OutputNanoAODFile%.root}}
    if ls ${{OutputNanoAODfile_noext}}*.root 1> /dev/null 2>&1; then
        echo "xrdcp -f ${{OutputNanoAODfile_noext}}*.root ${{OutputDir}}/${{OutputNanoAODFile}}"
        xrdcp -f ${{OutputNanoAODfile_noext}}*.root ${{OutputDir}}/${{OutputNanoAODFile}}
        echo "Removing local files after successful transfer: ${{OutputNanoAODfile_noext}}*.root"
        rm -f ${{OutputNanoAODfile_noext}}*.root
    elif [ -f "${{DerivedCfgOutputFile}}" ]; then
        echo "xrdcp -f ${{DerivedCfgOutputFile}} ${{OutputDir}}/${{OutputNanoAODFile}}"
        xrdcp -f "${{DerivedCfgOutputFile}}" "${{OutputDir}}/${{OutputNanoAODFile}}"
        echo "Removing local file after successful transfer: ${{DerivedCfgOutputFile}}"
        rm -f "${{DerivedCfgOutputFile}}"
    else
        echo "Error: ${{OutputNanoAODFile}} is not created"
        echo "Listing files in the current directory:"
        ls -ltr
    fi
fi

cd "${{basePath}}"
rm -rf "${{JobWorkDir}}"

echo "Ending job on " `date`
"""


jdl_file_template = """Executable = {CondorExecutable}.sh
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
Output = $(CondorLogPath)/log_$(Cluster)_$(Process).stdout
Error  = $(CondorLogPath)/log_$(Cluster)_$(Process).stderr
Log  = $(CondorLogPath)/log_$(Cluster)_$(Process).log
Arguments = $(Cluster) $(Process) $(configFile) $(inputMiniAOD) $(outputDirectory) $(outputFile) $(nEvents) $(inputRedirector)
queue 1 configFile, inputMiniAOD, outputDirectory, outputFile, nEvents, CondorLogPath, inputRedirector from {CondorExecutable}.txt
"""


slurm_file_template = """#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --output={top_log_directory}/nanoAOD_%A_%a.out
#SBATCH --error={top_log_directory}/nanoAOD_%A_%a.err
#SBATCH --account={account}
#SBATCH --partition={partition}
#SBATCH --qos={qos}
#SBATCH --array=1-{array_max}%{array_concurrency}
#SBATCH --ntasks={ntasks}
#SBATCH --cpus-per-task={cpus_per_task}
#SBATCH --mem={memory}
#SBATCH --time={walltime}
#SBATCH --get-user-env
#SBATCH --chdir={workdir}

set -euo pipefail

manifest="{manifest_path}"
payload_script="{payload_script}"

echo "Starting Slurm array job ${{SLURM_ARRAY_JOB_ID:-0}}, task ${{SLURM_ARRAY_TASK_ID}}"
echo "Running on $(hostname)"
echo "Working directory: $(pwd)"
echo "Manifest: $manifest"
echo "Payload: $payload_script"

line=$(sed -n "${{SLURM_ARRAY_TASK_ID}}p" "$manifest")
if [ -z "$line" ]; then
  echo "No manifest entry found for SLURM_ARRAY_TASK_ID=${{SLURM_ARRAY_TASK_ID}}"
  exit 1
fi

IFS=$'\t' read -r configFile inputMiniAOD outputDirectory outputFile nEvents CondorLogPath inputRedirector <<< "$line"
mkdir -p "$CondorLogPath"

task_stdout="${{CondorLogPath}}/payload_${{SLURM_ARRAY_JOB_ID:-0}}_${{SLURM_ARRAY_TASK_ID}}.stdout"
task_stderr="${{CondorLogPath}}/payload_${{SLURM_ARRAY_JOB_ID:-0}}_${{SLURM_ARRAY_TASK_ID}}.stderr"
exec > >(tee -a "$task_stdout")
exec 2> >(tee -a "$task_stderr" >&2)

echo "Redirecting payload stdout to $task_stdout"
echo "Redirecting payload stderr to $task_stderr"

bash "$payload_script" "${{SLURM_ARRAY_JOB_ID:-0}}" "$SLURM_ARRAY_TASK_ID" "$configFile" "$inputMiniAOD" "$outputDirectory" "$outputFile" "$nEvents" "$inputRedirector"
"""
