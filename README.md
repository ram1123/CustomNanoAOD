# CustomNanoAOD

This repository generates batch submission files for custom NanoAOD production on Purdue Gautschi or Condor. The practical starting point is an McM setup link, which you use to generate a CMSSW python cfg first. After that, this repository handles patching the cfg, wiring it into `config/config_HMuMu.json`, and generating Slurm or Condor submission files.

## Setup

Clone the repository and prepare the runtime environment:

```bash
git clone https://github.com/ram1123/CustomNanoAOD.git -b dev_HMuMu
cd CustomNanoAOD
source setup_env.sh
```

`setup_env.sh` does the following:

- activates `/depot/cms/kernels/python3`
- creates a VOMS proxy in `voms_proxy.txt`
- exports `X509_USER_PROXY`
- loads the CMSSW default environment

## End-to-End Flow

The typical workflow is:

1. Start from an McM setup link.
2. Download the setup script.
3. Run the setup script to generate the CMSSW python cfg.
4. Patch the generated cfg so it accepts runtime `inputFiles`, `outputFile`, and `maxEvents`.
5. Point `config/config_HMuMu.json` to that cfg.
6. Generate Slurm or Condor submission files with `condor_setup.py`.
7. Submit jobs and monitor logs.

## Step 1: Download the McM Setup Script

Example:

```bash
curl -L https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_setup/SMP-RunIISummer20UL18NanoAODv15-00034 -o SMP-RunIISummer20UL18NanoAODv15-00034_setup.sh
```

You can do the same for other prepids such as:

- `SMP-RunIISummer20UL17NanoAODv15-00042`
- `SMP-RunIISummer20UL18NanoAODv15-00034`
- `EGM-RunIISummer20UL16NanoAODv15-00001`
- `EGM-RunIISummer20UL16NanoAODAPVv15-00001`

## Step 2: Run the Setup Script

Run the downloaded setup script to generate the CMSSW python configuration:

```bash
bash SMP-RunIISummer20UL18NanoAODv15-00034_setup.sh
```

This produces the base CMSSW cfg that will later be used by the batch jobs.

## Repository Layout

- `condor_setup.py`: generates `.sh`, `.sub` or `.jdl`, and manifest `.txt` files
- `config/config_HMuMu.json`: maps year and sample type to the CMSSW config file
- `HMuMu/`: CMSSW python configs used at runtime
- `templates/`: shell and batch templates used by the generator
- `scripts/patch_generated_cmssw_cfg.py`: patches McM-generated configs to support runtime `inputFiles`, `outputFile`, and `maxEvents`

## Step 3: Patch the Generated CMSSW Python File

The generator reads `config/config_HMuMu.json`. Update this file so each year points to the correct CMSSW python config.

Example:

```json
{
  "cmsswConfigFileMap_MC": {
    "UL2018": "HMuMu/SMP-RunIISummer20UL18NanoAODv15-00034_1_cfg.py",
    "UL2017": "HMuMu/SMP-RunIISummer20UL17NanoAODv15-00042_1_cfg.py",
    "UL2016": "HMuMu/EGM-RunIISummer20UL16NanoAODv15-00001_1_cfg.py",
    "UL2016APV": "HMuMu/EGM-RunIISummer20UL16NanoAODAPVv15-00001_1_cfg.py"
  },
  "cmsswConfigFileMap_DATA": {},
  "replacementMap": {
    "_TuneCP5_PSweights_13TeV-amcatnloFXFX-pythia8": ""
  }
}
```

If you download a fresh McM setup script and generate a CMSSW cfg from it, patch the cfg before using it here:

```bash
python3 scripts/patch_generated_cmssw_cfg.py HMuMu/SMP-RunIISummer20UL18NanoAODv15-00034_1_cfg.py
```

That helper adds:

```python
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')
options.parseArguments()
```

```python
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)
```

- runtime replacements for `maxEvents`, `inputFiles`, `annotation`, and `outputFile`

## Step 4: Register the CMSSW Config in `config/config_HMuMu.json`

After patching, update `config/config_HMuMu.json` so each year points to the correct cfg. `condor_setup.py` reads this file to decide which CMSSW python config to pass to the batch jobs.

## Step 5: Generate Batch Files

Check the available options:

```bash
python3 condor_setup.py --help
```

Supported years:

- `UL2018`
- `UL2017`
- `UL2016`
- `UL2016APV`

Supported batch systems:

- `slurm`
- `condor`

Supported input modes:

- `txt`: one MiniAOD file per line
- `yaml`: DAS-driven sample discovery

### Slurm from a Text File

This is the recommended workflow for the current NanoAODv15 production.

```bash
python3 condor_setup.py \
  --batch_system slurm \
  --input_source txt \
  --input_txt /path/to/DYJets_UL2018.txt \
  --sample_type mc \
  --sample_name DYJets_NanoAOD \
  --files_per_job 1 \
  --year UL2018 \
  --input_redirector purdue \
  --eos_redirector purdue \
  --output_dir_name /store/user/rasharma/customNanoAODv15/UL2018/ \
  --condor_executable DYJets_UL2018_slurm \
  --slurm_mem 16000
```

This creates:

- `DYJets_UL2018_slurm.sh`
- `DYJets_UL2018_slurm.sub`
- `DYJets_UL2018_slurm.txt`

Submit with:

```bash
sbatch DYJets_UL2018_slurm.sub
```

### Condor from a YAML File

```bash
python3 condor_setup.py \
  --batch_system condor \
  --input_source yaml \
  --yaml HMuMu_DY_Samples.yaml \
  --year UL2018 \
  --output_dir_name /store/user/rasharma/customNanoAODv12 \
  --condor_executable HMuMu_UL2018
```

Submit with:

```bash
condor_submit HMuMu_UL2018.jdl
```

## Step 6: Submit Jobs

For Slurm:

```bash
sbatch DYJets_UL2018_slurm.sub
```

For Condor:

```bash
condor_submit HMuMu_UL2018.jdl
```

## Step 7: Logs and Monitoring

Slurm scheduler logs are written under:

```text
logs/<YEAR>/nanoAOD_<jobid>_<taskid>.out
logs/<YEAR>/nanoAOD_<jobid>_<taskid>.err
```

Payload logs are written under:

```text
logs/<YEAR>/<SAMPLE>/payload_<jobid>_<taskid>.stdout
logs/<YEAR>/<SAMPLE>/payload_<jobid>_<taskid>.stderr
```

Useful commands:

```bash
squeue -u $USER
sacct -j <jobid> --format=JobID,State,Elapsed,ExitCode
scontrol show job <jobid>
tail -F logs/UL2018/nanoAOD_<jobid>_<taskid>.out
tail -F logs/UL2018/<sample>/payload_<jobid>_<taskid>.stdout
```

## Resubmitting Failed Slurm Tasks

Inspect failed array tasks:

```bash
sacct -j <jobid> --format=JobID,State,ExitCode
```

Create a resubmission file from the original `.sub` and replace the array line with only the failed task IDs:

```bash
cp DYJets_UL2018_slurm.sub DYJets_UL2018_slurm_resubmit.sub
```

Then edit:

```text
#SBATCH --array=1-1000%200
```

to something like:

```text
#SBATCH --array=17,42,103%25
```

and submit:

```bash
sbatch DYJets_UL2018_slurm_resubmit.sub
```

For Condor resubmission, use:

```bash
python3 condor_resubmit.py -j <condor_jdl_file> -l <log_directory> -o <output_directory> -n <resubmission_count>
```

## Notes

- Regenerate the `.sh`, `.sub`, and manifest `.txt` files whenever you change anything under `templates/` or `config/`.
- Slurm jobs run in isolated scratch directories under `/tmp/$USER/` to avoid output filename collisions across years or samples.
- The payload removes the local ROOT file after a successful transfer to EOS.
- Remote output directories are created automatically when possible.
- Use real `MiniAOD` or `MiniAODSIM` inputs. A ROOT file having an `Events` tree is not enough if it does not contain the expected `slimmed*` products.
