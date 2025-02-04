# Setup

<!-- ```bash
cmsrel CMSSW_10_6_30
cd CMSSW_10_6_30/src
cmsenv
git cms-addpkg PhysicsTools

# copy `NanoTuples` directory from https://github.com/gqlcms/Customized_NanoAOD inside `PhysicsTools` directory
git clone git@github.com:gqlcms/Customized_NanoAOD.git /tmp/rasharma/Customized_NanoAOD
cp -r /tmp/rasharma/Customized_NanoAOD/NanoTuples PhysicsTools/
./PhysicsTools/NanoTuples/scripts/install_onnxruntime.sh
scram b -j8
``` -->

## Step - 1: Get current repository

```bash
git clone git@github.com:ram1123/CustomNanoAOD_HHWWgg.git
cd CustomNanoAOD_HHWWgg
```

## Step - 2: Setup CMSSW environment

```bash
cmsrel CMSSW_10_6_30
cd CMSSW_10_6_30/src
cmsenv
git cms-merge-topic -u ram1123:CMSSW_10_6_30_HHWWgg_nanoV9
./PhysicsTools/NanoTuples/scripts/install_onnxruntime.sh
scramv1 b -j 8
cd $CMSSW_BASE/../
```

## Step - 3: Run custom nanoAOD production

```bash
voms-proxy-init --voms cms --valid 168:00

cd ${CMSSW_BASE}/src
cmsenv
cd ../../
voms-proxy-init --voms cms --valid 168:00 --out $(pwd)/voms_proxy.txt
export X509_USER_PROXY=$(pwd)/voms_proxy.txt
source /cvmfs/cms.cern.ch/cmsset_default.sh
```

# Use the appropriate config file for different years
```bash
cmsRun cmssw_modified_config_files/HIG-RunIISummer20UL18NanoAODv9-02546_1_cfg.py maxEvents=-1 inputFiles=/store/mc/RunIISummer20UL18MiniAODv2/GluGluToRadionToHHTo2G2WTo2G4Q_M-1000_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/50000/04D3FBF0-A539-5143-9A1C-8D42A1D54C88.root  outputFile=HIG-RunIISummer20UL18NanoAODv9-02546.root
```

## Condor jobs instruction

To create the condor jobs submission script use the script [condor_setup.py](condor_setup.py). This script uses [YAML file](yaml_files/UL2018_XHH_Samples.yaml) having list of samples.

```bash
python3 condor_setup.py --help
```

**NOTE-1:** Check the config file before submitting the jobs: [config.json](config/config.json)
**NOTE-2:** The condor submission script distinguish between MC and data using the string of DAS name: "MINIAODSIM".

Some example commands to create the condor jobs submission script.

1. Create condor job submissioon script for debug:

    ```bash
    python3 condor_setup.py --condor_executable test_new --debug
    ```

    This will create a condor job submission script named `test_new.sh` and `test_new.jdl` in the current directory, having only one job.

2. Create condor job submissioon script for all samples that belong to UL2018 listed in yaml file [UL2018_XHH_Samples.yaml](yaml_files/UL2018_XHH_Samples.yaml):


    ```bash
    python3 condor_setup.py --condor_executable HHWWgg_UL2018 --yaml_file UL2018_XHH_Samples.yaml --year UL2018
    ```

## Failed condor jobs check and resbumit

[condor_resubmit.py](condor_resubmit.py): This script can be used to resubmit the failed condor jobs. It takes the condor log files as input and resubmits the failed jobs. It can be used as follows:

```bash
python condor_resubmit.py -j <condor_jdl_file> -l <log_directory> -o <output_directory> -n <resubmission_count>

# Example command:
python3 condor_resubmit.py -j HHbbgg_Signal_Mar2024.jdl -l logs/UL2018/EGamma_Run2018A/ -o /eos/user/r/rasharma/post_doc_ihep/double-higgs/nanoAODnTuples/nanoAOD_Mar2024/UL2018/EGamma_Run2018A -n 1
```

This will give you new jdl file. Then you can submit the new jdl file.


# 3 Feb 2022

```bash
python3 -m venv env_jobs_resubmit
source env_jobs_resubmit/bin/activate
# Install pandas dataframe
pip install pandas
```
