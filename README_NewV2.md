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
    ```

