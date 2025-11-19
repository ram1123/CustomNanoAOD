# Introduction

This framework is developed to get the custom NanoAODv12 for the HMuMu analysis.

# Setup

## Purdue Gautschi Cluster

***Basic Setup***

1. **Step-1**: Clone the repository
    ```bash
    git clone https://github.com/ram1123/CustomNanoAOD.git -b dev_HMuMu
    cd CustomNanoAOD
    source setup_env.sh

    # Before next step, prepare the file `HMuMu_DY_Samples.yaml` in the `yaml_files` directory.

    python3 condor_setup.py --condor_executable HMuMu_UL2018_NanoAODv12_MissingSamples --yaml HMuMu_DY_Samples.yaml --year UL2018 --output_dir_name /store/user/rasharma/Run2_CustomNanoAODv12

    python3 condor_setup.py --condor_executable HMuMu_UL2017_HLTbranchmissing --yaml HMuMU_Samples.yaml --year UL2017 --output_dir_name /store/user/rasharma/customNanoAOD_Gautschi_v2
    ```

    Once you get the .txt file you can setup the slurm job and submit it to the cluster.

# Slurm commands summary

1. Submit a job: `sbatch <job_file>.sub`
2. Check the status of a job: `squeue -u <username>`
3. Cancel a job: `scancel <job_id>`
4. Check the job history: `sacct -u <username> --starttime <start_time> --endtime <end_time>`
5. Check the job details: `scontrol show job <job_id>`
6. Check the job resource usage: `sstat -j <job_id> --format="JobID,MaxRSS,MaxVMSize,MaxDiskRead,MaxDiskWrite"`

