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
