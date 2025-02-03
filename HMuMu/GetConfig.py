import json
import subprocess
import sys
import re


def update_config_file(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    new_lines = []
    var_parsing_inserted = False
    message_logger_inserted = False

    # First, check if the VarParsing block is already present
    file_content = "".join(lines)
    if "VarParsing" in file_content:
        var_parsing_inserted = True

    # Process each line, doing replacements and inserting additional lines when needed.
    for i, line in enumerate(lines):
        # If we haven't inserted the VarParsing block, then after the initial import block insert it.
        if not var_parsing_inserted:
            # Detect end of initial import block (first non-import or non-comment line)
            if (
                re.match(r"^(import |from )", line)
                or re.match(r"^\s*#", line)
                or line.strip() == ""
            ):
                new_lines.append(line)
                continue
            else:
                # Insert VarParsing block here
                new_lines.append(
                    "\nfrom FWCore.ParameterSet.VarParsing import VarParsing\n"
                )
                new_lines.append("options = VarParsing('analysis')\n")
                new_lines.append("options.parseArguments()\n\n")
                var_parsing_inserted = True
        # Replace the parameter-setting lines if found
        if "input = cms.untracked.int32(" in line:
            new_lines.append("    input = cms.untracked.int32(options.maxEvents),\n")
            continue
        if "fileNames = cms.untracked.vstring(" in line:
            new_lines.append(
                "    fileNames = cms.untracked.vstring(options.inputFiles),\n"
            )
            continue
        if "annotation = cms.untracked.string(" in line:
            new_lines.append(
                "    annotation = cms.untracked.string('--python_filename nevts:'+str(options.maxEvents)),\n"
            )
            continue
        if "fileName = cms.untracked.string(" in line:
            new_lines.append(
                "    fileName = cms.untracked.string('file:'+options.outputFile),\n"
            )
            continue

        new_lines.append(line)

        # After the process declaration, insert the MessageLogger configuration if not already added.
        if not message_logger_inserted and "process = cms.Process(" in line:
            new_lines.append("\n# Print log file every 1000 events\n")
            new_lines.append(
                "process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)\n"
            )
            message_logger_inserted = True

    # Write back the updated file
    with open(file_path, "w") as f:
        f.writelines(new_lines)
    print(f"Updated configuration file: {file_path}")

def GetConfigFile():
    # Load the JSON file with era configurations
    with open('eras.json') as f:
        eras = json.load(f)

    # Load the template for the shell script (using Python's .format placeholders)
    with open('template.sh') as f:
        template_content = f.read()

    with open('template_data.sh') as f:
        template_content_data = f.read()

    # For each era, generate the shell script and the Condor submission file
    for era, params in eras.items():
        # Replace placeholders using Python's str.format method
        rendered_script = template_content.format(
            SCRIPT_NAME=(params["script_name"]).replace(".sh", "_test.sh"),
            PYTHON_CONFIG=params["python_config"],
            CONDITIONS=params["conditions"],
            FILEIN=params["filein"],
            FILEOUT=params["fileout"],
            ERA=params["era"]
        )

        # Write out the era-specific script
        script_filename = params["script_name"]
        with open(script_filename, 'w') as outf:
            outf.write(rendered_script)
        print(f"Generated {script_filename}")

        # Run the script
        subprocess.run(['bash', script_filename])

        update_config_file(params["python_config"])

        rendered_script_data = template_content_data.format(
            SCRIPT_NAME=(params["script_name"]).replace(".sh", "_test_data.sh"),
            PYTHON_CONFIG=params["python_config"].replace("cfg.py", "data_cfg.py"),
            CONDITIONS_DATA=params["conditions_data"],
            FILEIN=params["filein"],
            FILEOUT=params["fileout"],
            ERA=params["era"],
        )

        # Write out the era-specific script
        script_filename = params["script_name"].replace(".sh", "_data.sh")
        with open(script_filename, 'w') as outf:
            outf.write(rendered_script_data)
        print(f"Generated {script_filename}")

        # Run the script
        subprocess.run(['bash', script_filename])

        update_config_file(params["python_config"].replace("cfg.py", "data_cfg.py"))

if __name__ == "__main__":
    GetConfigFile()
