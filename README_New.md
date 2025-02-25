# Setup

```bash
git clone https://github.com/ram1123/CustomNanoAOD.git -b dev_HMuMu
cd CustomNanoAOD
source /cvmfs/cms.cern.ch/cmsset_default.sh
voms-proxy-init --voms cms --valid 168:00 --out $(pwd)/voms_proxy.txt
export X509_USER_PROXY=$(pwd)/voms_proxy.txt
```

# TO run the resubmit jobs
```bash
source /etc/profile.d/modules.sh
module --force purge
module load anaconda/2020.11
conda activate /depot/cms/kernels/coffea_latest
```

# Get python virtual environment
```bash
python -m venv venv
source venv/bin/activate
deactivate
```


```bash
python3 condor_setup.py --condor_executable HMuMu_UL2018_3Feb_AllJobs --yaml HMuMU_Samples.yaml --year UL2018 --output_dir_name /store/user/rasharma/customNanoAOD_Others
python3 condor_setup.py --condor_executable HMuMu_UL2017_3Feb_AllJobs --yaml HMuMU_Samples.yaml --year UL2017 --output_dir_name /store/user/rasharma/customNanoAOD_Gautschi

python3 condor_setup.py --condor_executable HMuMu_UL2017_8Feb_2016APV --yaml HMuMU_Samples.yaml --year UL2016APV --output_dir_name /store/user/rasharma/customNanoAOD_Gautschi_2016APV
python3 condor_setup.py --condor_executable HMuMu_UL2017_8Feb_2016 --yaml HMuMU_Samples.yaml --year UL2016 --output_dir_name /store/user/rasharma/customNanoAOD_Gautschi_2016
```

```bash
sbatch slurm_setup_multipleJobs.sub
```

# Text replace commands

```bash
sed -i 's/logs_20Feb/logs_23Feb/g' *.sub
sed -i 's/21Feb/24Feb/g' *.sub
```


# TODO
- [ ] Add option to recognize the miniAOD/nanoAOD DAS path. Then proceed with it.
