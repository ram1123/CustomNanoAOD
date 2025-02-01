import json
import subprocess

# Load the JSON file with era configurations
with open('eras.json') as f:
    eras = json.load(f)

# Load the template for the shell script (using Python's .format placeholders)
with open('template.sh') as f:
    template_content = f.read()

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
