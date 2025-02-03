import argparse
import os
import json
from pathlib import Path
import subprocess

from templates.condor_script_template import sh_file_template_HMuMu
from templates.condor_script_template import jdl_file_template

parser = argparse.ArgumentParser(description="Generate Condor script for HH sample")

parser.add_argument(
    "--condor_executable",
    type=str,
    default="HH_WWgg_Signal_v2",
    help="Name of the Condor executable",
)
parser.add_argument(
    "--TopLogDirectory", type=str, default="logs", help="Path for the log file"
)
# add eos redirector:  root://eosuser.cern.ch/ or root://cms-xrd-global.cern.ch/
# add only two options: 1. eos redirector and 2. for global redirector
parser.add_argument(
    "--eos_redirector",
    type=int,
    default=2,
    choices=[1, 2, 3],
    help="""EOS redirector:
                                                            1. EOS redirectory: root://eosuser.cern.ch/
                                                            2. Purdue redirector: root://eos.cms.rcac.purdue.edu/
                                                            3. Global redirector: root://cms-xrd-global.cern.ch/
                                                            """,
)
parser.add_argument(
    "--output_dir_name",
    type=str,
    default="/store/user/rasharma/customNanoAOD",
    help="Path for the output directory",
    # FIXME: Update to generalise the path for condor/slurm
)
parser.add_argument(
    "--condor_queue",
    type=str,
    default="tomorrow",
    choices=[
        "espresso",
        "microcentury",
        "longlunch",
        "workday",
        "tomorrow",
        "testmatch",
        "nextweek",
    ],
    help="Name of the Condor queue",
)
parser.add_argument("--queue", type=int, default=1, help="Number of jobs")
parser.add_argument(
    "--year",
    type=str,
    default="UL2018",
    choices=["UL2018", "UL2017", "UL2016", "UL2016APV"],
    help="Year of the sample",
)
parser.add_argument("--yaml", type=str, default="UL2018_XHH_Samples.yaml")
parser.add_argument("--yamlPath", type=str, default="yaml_files")
parser.add_argument("--maxEvents", type=int, default=-1, help="Number of events to run")
parser.add_argument(
    "--debug",
    action="store_true",
    default=False,
    help="If this is true, only one job will be submitted",
)

args = parser.parse_args()

CondorExecutable = args.condor_executable
TopLogDirectory = args.TopLogDirectory
outputDirName = args.output_dir_name
CondorQueue = args.condor_queue
queue = args.queue
if args.eos_redirector == 1:
    xrd_redirector = "root://eosuser.cern.ch/"
elif args.eos_redirector == 2:
    xrd_redirector = "root://eos.cms.rcac.purdue.edu/"
else:
    xrd_redirector = "root://cms-xrd-global.cern.ch/"

if args.debug:
    args.maxEvents = 100

# Load configuration from json file
with open("config/config_HMuMu.json", "r") as f:
    config_data = json.load(f)

cmsswConfigFileMap_MC = config_data["cmsswConfigFileMap_MC"]
cmsswConfigFileMap_DATA = config_data["cmsswConfigFileMap_DATA"]
replacementMap = config_data["replacementMap"]

# Create the shell script
condor_executable_path = Path(f"{CondorExecutable}.sh")
with condor_executable_path.open("w") as fout:
    fout.write(sh_file_template_HMuMu.format(test="Job started...", maxEvents=args.maxEvents))

# Create the job description file
condor_jdl_path = Path(f"{CondorExecutable}.jdl")
with condor_jdl_path.open("w") as fout:
    fout.write(jdl_file_template.format(
        CondorExecutable=CondorExecutable,
        cmsswConfigFile=cmsswConfigFileMap_MC[args.year] + ', ' + cmsswConfigFileMap_DATA[args.year],
                                            CondorQueue = CondorQueue))

condor_txt_path = Path(f"{CondorExecutable}.txt")
with condor_txt_path.open("w") as fout:
    # Loop over all the sample listed in UL18_signal.json file
    import yaml

    # Open the YAML file
    yamlFileWithPath = Path(args.yamlPath) / args.yaml
    try:
        with open(yamlFileWithPath, "r") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: YAML file {yamlFileWithPath} not found.")
        exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML file: {e}")
        exit(1)

    count_jobs = 0
    isMC = False
    # Loop over all the keys in the YAML file
    # for Era in data.keys():
    for sample in data[args.year]:
        Era = args.year
        print("Era: {}, sample: {}, isMC: {}".format(Era, sample, isMC))
        dirName = Era
        sample_name = sample.split("/")[1]
        if not isMC:
            sample_name = (
                sample_name + "_" + sample.split("/")[2].split("-")[0]
            )  # Example: EGamma_Run2018A
        print("==> sample_name = ", sample_name)
        for key, value in replacementMap.items():
            sample_name = sample_name.replace(
                key, value
            )  # Example:GluGluToRadionToHHTo2G2WTo2G4Q_M-1200
        campaign = sample.split("/")[2].split("-")[0]
        print("==> sample_name = ", sample_name)
        print("==> campaign = ", campaign)

        # Create the output path, where the nanoAOD will be stored
        output_rootfile_path = Path(outputDirName) / Era / sample_name
        try:
            # output_rootfile_path.mkdir(parents=True, exist_ok=True)
            os.system('gfal-mkdir -p davs://eos.cms.rcac.purdue.edu:9000{}'.format(output_rootfile_path))
            # FIXME: Improve this part
        except OSError as e:
            print(f"Error: Could not create directory {output_rootfile_path}: {e}")
            exit(1)

        # Create the output log file path
        output_logfile_path = Path(TopLogDirectory) / Era / sample_name
        try:
            output_logfile_path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"Error: Could not create directory {output_logfile_path}: {e}")
            exit(1)

        cmd = f'dasgoclient --query="parent dataset={sample}"'
        try:
            sample_miniAOD = subprocess.check_output(cmd, shell=True).decode()
            print("sample_miniAOD:{}___".format(sample_miniAOD.split()[0]))
        except subprocess.CalledProcessError as e:
            print(f"Error: dasgoclient query failed: {e}")
            exit(1)

        cmd = f'dasgoclient --query="file dataset={sample_miniAOD.split()[0]}"'
        try:
            output = subprocess.check_output(cmd, shell=True).decode()
        except subprocess.CalledProcessError as e:
            print(f"Error: dasgoclient query failed: {e}")
            exit(1)

        # print("output:", output)
        # exit()

        # If the sample contains "MINIAODSIM", then it is MC sample otherwise it is data
        if "MINIAODSIM" in sample_miniAOD.split()[0]:
            isMC = True
            cmsswConfigFileMap = cmsswConfigFileMap_MC
        else:
            isMC = False
            cmsswConfigFileMap = cmsswConfigFileMap_DATA

        count_root_files = 0
        for root_file in output.split():
            if args.debug:
                print("root_file: ", root_file)
            count_root_files += 1
            count_jobs += 1

            fout.write(
                "{configFile} {inputFile} {outputDir} {maxEvents} {logFile}\n".format(
                    configFile=cmsswConfigFileMap[args.year].split("/")[-1],
                    inputFile=root_file,
                    outputDir=xrd_redirector + str(output_rootfile_path),
                    maxEvents=args.maxEvents,
                    logFile=output_logfile_path,
                )
            )

            if args.debug:
                break
        if args.debug:
            break

print("\nTotal number of jobs: ", count_jobs)

# Make the shell script executable
os.system(f"chmod 777 {CondorExecutable}.sh")

# Print the steps to submit the job
print("\n#===> Set Proxy Using:")
print("voms-proxy-init --voms cms --valid 168:00")
print(
    "\n# It is assumed that the proxy is created in file: /tmp/x509up_u48539. Update this in below two lines:"
)
print("cp /tmp/x509up_u48539 ~/")
print("export X509_USER_PROXY=~/x509up_u48539")
print("\n#Submit jobs:")
print("condor_submit " + CondorExecutable + ".jdl")
