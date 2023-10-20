import argparse
import os
from condor_script_template import sh_file_template
from condor_script_template import jdl_file_template_part1of2
from condor_script_template import jdl_file_template_part2of2

parser = argparse.ArgumentParser(description='Generate Condor script for HH sample')

parser.add_argument('--condor_executable', type=str, default="HH_WWgg_Signal_v2",
                    help='Name of the Condor executable')
parser.add_argument('--TopLogDirectory', type=str, default="Logs",
                    help='Path for the log file')
parser.add_argument('--output_dir_name', type=str, default="/eos/user/r/rasharma/post_doc_ihep/double-higgs/nanoAODnTuples/nanoAOD_Oct19/",
                    help='Path for the output directory')
parser.add_argument('--condor_queue', type=str, default="testmatch",
                    help='Name of the Condor queue: espresso, testmatch')
parser.add_argument('--queue', type=int, default=1,
                    help='Number of jobs')
parser.add_argument('--year', type=str, default="UL2018", choices=['UL2018', 'UL2017', 'UL2016', 'UL2016APV'],
                    help='Year of the sample')
parser.add_argument('--yaml', type=str, default="UL2018_XHH_Samples.yaml", )
parser.add_argument('--maxEvents', type=int, default=-1,
                    help='Number of events to run')
parser.add_argument('--debug', action='store_true')

args = parser.parse_args()

CondorExecutable = args.condor_executable
TopLogDirectory = args.TopLogDirectory
outputDirName = args.output_dir_name
CondorQueue = args.condor_queue
queue = args.queue

if args.debug:
     args.maxEvents = 100

cmsswConfigFileMap = {
    'UL2018': 'HIG-RunIISummer20UL18NanoAODv9-02546_1_cfg.py',
    'UL2017': 'HIG-RunIISummer20UL17NanoAODv9-02407_1_cfg.py',
    'UL2016': 'HIG-RunIISummer20UL16NanoAODv9-02412_1_cfg.py',
    'UL2016APV': 'HIG-RunIISummer20UL16NanoAODAPVv9-01726_1_cfg.py'
}

replacementMap = {
    '_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8': ''
}

# Create the shell script
with open(f"{CondorExecutable}.sh","w") as fout:
    fout.write(sh_file_template.format(test="Job started...", maxEvents=args.maxEvents))

# Create the job description file
with open(f"{CondorExecutable}.jdl","w") as fout:
    fout.write(jdl_file_template_part1of2.format(
                                            CondorExecutable = CondorExecutable,
                                            cmsswConfigFile = cmsswConfigFileMap[args.year],
                                            CondorQueue = CondorQueue))

    # Loop over all the sample listed in UL18_signal.json file
    import yaml


    # Open the YAML file
    with open(args.yaml, "r") as f:
        data = yaml.safe_load(f)
        print("data: {}".format(data))

    count_jobs = 0
    # Loop over all the keys in the YAML file
    # for Era in data.keys():
    for sample in data[args.year]:
            Era = args.year
            print("Era: {}, sample: {}".format(Era, sample))
            # sample_name = sample
            # sample_name = lines.split('/')[1]
            dirName = Era
            sample_name = sample.split('/')[1]
            print("==> sample_name = ",sample_name)
            for key, value in replacementMap.items():
                sample_name = sample_name.replace(key, value)
            # sample_name = Era
            campaign = sample.split('/')[2].split('-')[0]
            print("==> sample_name = ",sample_name)
            print("==> campaign = ",campaign)

            # Create the output path, where the nanoAOD will be stored
            output_rootfile_path =  f"{outputDirName}/{Era}/{sample_name}"
            os.makedirs(output_rootfile_path, exist_ok=True)

            # Create the output log file path
            output_logfile_path = f"{TopLogDirectory}/{Era}/{sample_name}"
            os.makedirs(output_logfile_path, exist_ok=True)

            xrd_redirector = 'root://cms-xrd-global.cern.ch/'
            output = os.popen('dasgoclient --query="file dataset='+sample+'"').read()

            count_root_files = 0
            for root_file in output.split():
                #print "=> ",root_file
                count_root_files+=1
                count_jobs += 1

                # Write the job description to the file
                fout.write(jdl_file_template_part2of2.format(
                                                CondorLogPath = output_logfile_path,
                                                cmsswConfigFile = cmsswConfigFileMap[args.year],
                                                InputMiniAODFile = root_file,
                                                OutputNanoAODFile = f"{Era}_$(Cluster)_$(Process).root",
                                                outDir = output_rootfile_path,
                                                queue = queue
                                                ))
                if args.debug:
                    break

# Make the shell script executable
os.system(f"chmod 777 {CondorExecutable}.sh")

# Print the steps to submit the job
print("\n#===> Set Proxy Using:")
print("voms-proxy-init --voms cms --valid 168:00")
print("\n# It is assumed that the proxy is created in file: /tmp/x509up_u48539. Update this in below two lines:")
print("cp /tmp/x509up_u48539 ~/")
print("export X509_USER_PROXY=~/x509up_u48539")
print("\n#Submit jobs:")
print("condor_submit "+CondorExecutable+".jdl")
