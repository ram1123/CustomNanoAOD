import argparse
import json
import subprocess
from pathlib import Path

from templates.condor_script_template import jdl_file_template
from templates.condor_script_template import sh_file_template_HMuMu
from templates.condor_script_template import slurm_file_template


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate batch submission files for custom NanoAOD production"
    )
    parser.add_argument(
        "--condor_executable",
        type=str,
        default="HH_WWgg_Signal_v2",
        help="Base name for generated submission files",
    )
    parser.add_argument(
        "--TopLogDirectory", type=str, default="logs", help="Top-level log directory"
    )
    parser.add_argument(
        "--batch_system",
        type=str,
        default="condor",
        choices=["condor", "slurm"],
        help="Batch system to target",
    )
    parser.add_argument(
        "--input_source",
        type=str,
        default="yaml",
        choices=["yaml", "txt"],
        help="Build jobs from DAS-discovered datasets in YAML or from a local text file of MiniAOD files",
    )
    parser.add_argument(
        "--eos_redirector",
        type=str,
        default="purdue",
        choices=["cern", "purdue", "global"],
        help="Redirector used for output writes",
    )
    parser.add_argument(
        "--input_redirector",
        type=str,
        default="global",
        choices=["cern", "purdue", "global", "none"],
        help="Redirector used when reading input files that are listed as /store/... paths",
    )
    parser.add_argument(
        "--output_dir_name",
        type=str,
        default="/store/user/rasharma/customNanoAOD",
        help="Remote output directory",
    )
    parser.add_argument(
        "--skip_remote_mkdir",
        action="store_true",
        default=False,
        help="Skip creating the remote output directory before generating job files",
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
        help="Condor job flavour",
    )
    parser.add_argument(
        "--slurm_partition",
        type=str,
        default="cpu",
        help="Slurm partition name",
    )
    parser.add_argument(
        "--slurm_account",
        type=str,
        default="cms",
        help="Slurm account name",
    )
    parser.add_argument(
        "--slurm_qos",
        type=str,
        default="standby",
        help="Slurm QoS",
    )
    parser.add_argument(
        "--slurm_time",
        type=str,
        default="03:50:00",
        help="Slurm walltime in Slurm format, for example 04:00:00 or 1-00:00:00",
    )
    parser.add_argument(
        "--slurm_mem",
        type=str,
        default="2010",
        help="Slurm memory request",
    )
    parser.add_argument(
        "--slurm_ntasks",
        type=int,
        default=1,
        help="Slurm ntasks request",
    )
    parser.add_argument(
        "--slurm_cpus_per_task",
        type=int,
        default=1,
        help="Slurm CPU request",
    )
    parser.add_argument(
        "--slurm_array_concurrency",
        type=int,
        default=200,
        help="Maximum number of concurrent Slurm array tasks",
    )
    parser.add_argument("--queue", type=int, default=1, help="Unused legacy option")
    parser.add_argument(
        "--year",
        type=str,
        default="UL2018",
        choices=["UL2018", "UL2017", "UL2016", "UL2016APV"],
        help="Year of the sample",
    )
    parser.add_argument("--yaml", type=str, default="UL2018_XHH_Samples.yaml")
    parser.add_argument("--yamlPath", type=str, default="yaml_files")
    parser.add_argument(
        "--input_txt",
        type=str,
        help="Text file containing one MiniAOD root file path per line",
    )
    parser.add_argument(
        "--sample_type",
        type=str,
        default="mc",
        choices=["mc", "data"],
        help="Used in txt mode to choose the CMSSW config family",
    )
    parser.add_argument(
        "--sample_name",
        type=str,
        help="Optional sample label for txt mode; defaults to the txt filename stem",
    )
    parser.add_argument(
        "--files_per_job",
        type=int,
        default=1,
        help="How many input MiniAOD files to bundle into one job",
    )
    parser.add_argument(
        "--maxEvents", type=int, default=-1, help="Number of events to run"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="If true, only one job is emitted",
    )
    return parser.parse_args()


def load_yaml(yaml_path):
    import yaml

    try:
        with yaml_path.open("r") as handle:
            return yaml.safe_load(handle)
    except FileNotFoundError:
        raise SystemExit(f"Error: YAML file {yaml_path} not found.")
    except yaml.YAMLError as exc:
        raise SystemExit(f"Error: Invalid YAML file {yaml_path}: {exc}")


def run_command(command):
    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip() if exc.stderr else ""
        stdout = exc.stdout.strip() if exc.stdout else ""
        details = stderr or stdout or str(exc)
        raise SystemExit(f"Error: command failed: {' '.join(command)}\n{details}")

    return result.stdout.strip()


def get_redirector_info(redirector_name):
    redirector_map = {
        "cern": {
            "xrd": "root://eosuser.cern.ch/",
            "mkdir_host": "root://eosuser.cern.ch",
        },
        "purdue": {
            "xrd": "root://eos.cms.rcac.purdue.edu/",
            "mkdir_host": "root://eos.cms.rcac.purdue.edu",
        },
        "global": {
            "xrd": "root://cms-xrd-global.cern.ch/",
            "mkdir_host": None,
        },
        "none": {
            "xrd": "",
            "mkdir_host": None,
        },
    }
    return redirector_map[redirector_name]


def ensure_remote_directory(output_rootfile_path, redirector_info):
    mkdir_host = redirector_info["mkdir_host"]
    if mkdir_host is None:
        print(
            "Warning: skipping remote directory creation for the selected output redirector."
        )
        return

    run_command(["xrdfs", mkdir_host, "mkdir", "-p", str(output_rootfile_path)])


def build_output_rootfile_path(base_output_dir, era, sample_name):
    base_path = Path(base_output_dir)
    if base_path.name == era:
        return base_path / sample_name
    return base_path / era / sample_name


def query_parent_dataset(sample):
    output = run_command(["dasgoclient", "--query", f"parent dataset={sample}"])
    datasets = output.split()
    if not datasets:
        raise SystemExit(f"Error: no parent dataset found for sample {sample}")
    return datasets[0]


def query_files(dataset):
    output = run_command(["dasgoclient", "--query", f"file dataset={dataset}"])
    files = output.split()
    if not files:
        raise SystemExit(f"Error: no files found for dataset {dataset}")
    return files


def resolve_input_dataset(sample):
    if "MINIAOD" in sample:
        return sample
    return query_parent_dataset(sample)


def get_sample_name(sample, is_mc, replacement_map):
    sample_parts = sample.split("/")
    sample_name = sample_parts[1]
    if not is_mc:
        sample_name = f"{sample_name}_{sample_parts[2].split('-')[0]}"

    for key, value in replacement_map.items():
        sample_name = sample_name.replace(key, value)

    return sample_name


def chunk_list(items, chunk_size):
    return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]


def get_config_file(config_map, year, label):
    try:
        return config_map[year]
    except KeyError as exc:
        raise SystemExit(
            f"Error: missing {label} CMSSW config for year {year} in config/config_HMuMu.json"
        ) from exc


def write_payload_script(output_prefix, max_events):
    payload_path = Path(f"{output_prefix}.sh")
    with payload_path.open("w") as handle:
        handle.write(
            sh_file_template_HMuMu.format(test="Job started...", maxEvents=max_events)
        )
    payload_path.chmod(0o755)
    return payload_path


def write_condor_jdl(output_prefix, condor_queue, transfer_config_files):
    jdl_path = Path(f"{output_prefix}.jdl")
    with jdl_path.open("w") as handle:
        handle.write(
            jdl_file_template.format(
                CondorExecutable=output_prefix,
                cmsswConfigFile=", ".join(transfer_config_files),
                CondorQueue=condor_queue,
            )
        )
    return jdl_path


def write_slurm_script(output_prefix, args, total_jobs):
    slurm_path = Path(f"{output_prefix}.sub")
    top_log_directory = Path(args.TopLogDirectory).resolve()
    top_log_directory.mkdir(parents=True, exist_ok=True)
    workdir = Path.cwd().resolve()
    manifest_path = (workdir / f"{output_prefix}.txt").resolve()
    payload_path = (workdir / f"{output_prefix}.sh").resolve()

    with slurm_path.open("w") as handle:
        handle.write(
            slurm_file_template.format(
                job_name=output_prefix,
                array_max=total_jobs,
                array_concurrency=args.slurm_array_concurrency,
                top_log_directory=top_log_directory,
                account=args.slurm_account,
                cpus_per_task=args.slurm_cpus_per_task,
                memory=args.slurm_mem,
                ntasks=args.slurm_ntasks,
                walltime=args.slurm_time,
                partition=args.slurm_partition,
                qos=args.slurm_qos,
                workdir=workdir,
                manifest_path=manifest_path,
                payload_script=payload_path,
            )
        )
    slurm_path.chmod(0o755)
    return slurm_path


def format_manifest_entry(
    config_file, input_files, output_dir, output_file, max_events, log_dir, input_redirector
):
    return "\t".join(
        [
            config_file,
            ",".join(input_files),
            output_dir,
            output_file,
            str(max_events),
            str(log_dir),
            input_redirector,
        ]
    )


def add_entries_for_sample(
    manifest_entries,
    input_files,
    config_file,
    output_rootfile_path,
    output_logfile_path,
    input_redirector,
    sample_name,
    files_per_job,
    max_events,
    debug,
):
    chunked_files = chunk_list(input_files, files_per_job)
    if debug:
        chunked_files = chunked_files[:1]

    for chunk_index, file_chunk in enumerate(chunked_files, start=1):
        output_file = f"{sample_name}_chunk{chunk_index:04d}.root"
        manifest_entries.append(
            format_manifest_entry(
                config_file=config_file,
                input_files=file_chunk,
                output_dir=str(output_rootfile_path),
                output_file=output_file,
                max_events=max_events,
                log_dir=output_logfile_path,
                input_redirector=input_redirector,
            )
        )


def build_entries_from_yaml(
    args,
    replacement_map,
    cmssw_config_file_map_mc,
    cmssw_config_file_map_data,
    output_redirector_info,
    input_redirector,
):
    yaml_file_with_path = Path(args.yamlPath) / args.yaml
    data = load_yaml(yaml_file_with_path)
    if args.year not in data:
        raise SystemExit(
            f"Error: year {args.year} not found in YAML file {yaml_file_with_path}"
        )

    manifest_entries = []
    print("===> Year:", args.year)
    for sample in data[args.year]:
        era = args.year
        input_dataset = resolve_input_dataset(sample)
        is_mc = "MINIAODSIM" in input_dataset
        cmssw_config_file_map = (
            cmssw_config_file_map_mc if is_mc else cmssw_config_file_map_data
        )
        config_file = get_config_file(
            cmssw_config_file_map, args.year, "MC" if is_mc else "DATA"
        )

        sample_name = get_sample_name(sample, is_mc, replacement_map)
        campaign = sample.split("/")[2].split("-")[0]
        print(f"Era: {era}, sample: {sample}, isMC: {is_mc}")
        print("==> sample_name =", sample_name)
        print("==> campaign =", campaign)
        print("==> input dataset =", input_dataset)

        output_rootfile_path = build_output_rootfile_path(
            args.output_dir_name, era, sample_name
        )
        if not args.skip_remote_mkdir:
            ensure_remote_directory(output_rootfile_path, output_redirector_info)

        output_logfile_path = Path(args.TopLogDirectory) / era / sample_name
        output_logfile_path.mkdir(parents=True, exist_ok=True)

        root_files = query_files(input_dataset)
        add_entries_for_sample(
            manifest_entries=manifest_entries,
            input_files=root_files,
            config_file=Path(config_file).name,
            output_rootfile_path=output_redirector_info["xrd"] + str(output_rootfile_path),
            output_logfile_path=output_logfile_path,
            input_redirector=input_redirector,
            sample_name=sample_name,
            files_per_job=args.files_per_job,
            max_events=args.maxEvents,
            debug=args.debug,
        )

        if args.debug:
            break

    return manifest_entries


def read_input_txt(txt_path):
    try:
        lines = [
            line.strip()
            for line in txt_path.read_text().splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
    except FileNotFoundError:
        raise SystemExit(f"Error: input txt file {txt_path} not found.")

    if not lines:
        raise SystemExit(f"Error: input txt file {txt_path} has no usable entries.")
    return lines


def normalize_input_file_path(path):
    stripped = path.strip()
    eos_prefixes = [
        "/eos/purdue/store/",
        "/eos/cms/store/",
        "/eos/user/store/",
    ]
    for prefix in eos_prefixes:
        if stripped.startswith(prefix):
            return "/store/" + stripped[len(prefix) :]
    return stripped


def build_entries_from_txt(
    args,
    cmssw_config_file_map_mc,
    cmssw_config_file_map_data,
    output_redirector_info,
    input_redirector,
):
    if not args.input_txt:
        raise SystemExit("Error: --input_txt is required when --input_source txt is used.")

    txt_path = Path(args.input_txt)
    input_files = [normalize_input_file_path(path) for path in read_input_txt(txt_path)]
    sample_name = args.sample_name or txt_path.stem
    is_mc = args.sample_type == "mc"
    cmssw_config_file_map = (
        cmssw_config_file_map_mc if is_mc else cmssw_config_file_map_data
    )
    config_file = get_config_file(
        cmssw_config_file_map, args.year, "MC" if is_mc else "DATA"
    )

    output_rootfile_path = build_output_rootfile_path(
        args.output_dir_name, args.year, sample_name
    )
    if not args.skip_remote_mkdir:
        ensure_remote_directory(output_rootfile_path, output_redirector_info)

    output_logfile_path = Path(args.TopLogDirectory) / args.year / sample_name
    output_logfile_path.mkdir(parents=True, exist_ok=True)

    manifest_entries = []
    add_entries_for_sample(
        manifest_entries=manifest_entries,
        input_files=input_files,
        config_file=Path(config_file).name,
        output_rootfile_path=output_redirector_info["xrd"] + str(output_rootfile_path),
        output_logfile_path=output_logfile_path,
        input_redirector=input_redirector,
        sample_name=sample_name,
        files_per_job=args.files_per_job,
        max_events=args.maxEvents,
        debug=args.debug,
    )
    print(f"===> txt input: {txt_path}")
    print(f"===> sample_name: {sample_name}")
    print(f"===> sample_type: {args.sample_type}")
    print(f"===> files discovered: {len(input_files)}")
    return manifest_entries


def main():
    args = parse_args()
    if args.debug:
        args.maxEvents = 100
    if args.files_per_job < 1:
        raise SystemExit("Error: --files_per_job must be at least 1.")

    config_path = Path("config/config_HMuMu.json")
    with config_path.open("r") as handle:
        config_data = json.load(handle)

    cmssw_config_file_map_mc = config_data["cmsswConfigFileMap_MC"]
    cmssw_config_file_map_data = config_data["cmsswConfigFileMap_DATA"]
    replacement_map = config_data["replacementMap"]

    output_redirector_info = get_redirector_info(args.eos_redirector)
    input_redirector = get_redirector_info(args.input_redirector)["xrd"]

    output_prefix = args.condor_executable
    payload_path = write_payload_script(output_prefix, args.maxEvents)

    transfer_config_files = []
    if args.year in cmssw_config_file_map_mc:
        transfer_config_files.append(cmssw_config_file_map_mc[args.year])
    if args.year in cmssw_config_file_map_data:
        transfer_config_files.append(cmssw_config_file_map_data[args.year])

    if args.input_source == "yaml":
        manifest_entries = build_entries_from_yaml(
            args=args,
            replacement_map=replacement_map,
            cmssw_config_file_map_mc=cmssw_config_file_map_mc,
            cmssw_config_file_map_data=cmssw_config_file_map_data,
            output_redirector_info=output_redirector_info,
            input_redirector=input_redirector,
        )
    else:
        manifest_entries = build_entries_from_txt(
            args=args,
            cmssw_config_file_map_mc=cmssw_config_file_map_mc,
            cmssw_config_file_map_data=cmssw_config_file_map_data,
            output_redirector_info=output_redirector_info,
            input_redirector=input_redirector,
        )

    if not manifest_entries:
        raise SystemExit("Error: no jobs were generated.")

    manifest_path = Path(f"{output_prefix}.txt")
    with manifest_path.open("w") as handle:
        handle.write("\n".join(manifest_entries) + "\n")

    print("\nTotal number of jobs:", len(manifest_entries))

    if args.batch_system == "condor":
        write_condor_jdl(output_prefix, args.condor_queue, transfer_config_files)
        print("\n#===> Set Proxy Using:")
        print("voms-proxy-init --voms cms --valid 168:00")
        print("\n#Submit jobs:")
        print(f"condor_submit {output_prefix}.jdl")
    else:
        write_slurm_script(output_prefix, args, len(manifest_entries))
        print("\n#Submit jobs:")
        print(f"sbatch {output_prefix}.sub")

    print("\nGenerated files:")
    print(f"- {payload_path}")
    print(f"- {manifest_path}")
    if args.batch_system == "condor":
        print(f"- {output_prefix}.jdl")
    else:
        print(f"- {output_prefix}.sub")


if __name__ == "__main__":
    main()
