# Ways to find failed jobs

```bash
grep -rn "An exception of category 'FileReadError' occurred while" *.err
grep -rn "An exception of category 'FileOpenError' occurred while" *.err
```

# 4 April 2025
```bash
python condor_setup.py --condor_executable UL2018_Queue2 --eos_redirector purdue --output_dir_name /store/user/rasharma/customNanoAOD_Others/ --year UL2018 --yamlPath yaml_files --yaml HMuMU_Samples.yaml --maxEvents -1
python condor_setup.py --condor_executable UL2017_Queue2 --eos_redirector purdue --output_dir_name /store/user/rasharma/customNanoAOD_Gautschi_v2/ --year UL2017 --yamlPath yaml_files --yaml HMuMU_Samples.yaml --maxEvents -1
python condor_setup.py --condor_executable UL2016APV_Queue2 --eos_redirector purdue --output_dir_name /store/user/rasharma/customNanoAOD_Gautschi_2016APV/ --year UL2016APV --yamlPath yaml_files --yaml HMuMU_Samples.yaml --maxEvents -1
python condor_setup.py --condor_executable UL2016_Queue2 --eos_redirector purdue --output_dir_name /store/user/rasharma/customNanoAOD_Gautschi_2016/ --year UL2016 --yamlPath yaml_files --yaml HMuMU_Samples.yaml --maxEvents -1
```


# 30 March 2025

```bash
python condor_setup.py --condor_executable UL2018-GT36 --eos_redirector purdue --output_dir_name /store/user/rasharma/customNanoAOD_GT36 --year UL2018 --yamlPath yaml_files --yaml HMuMU_Samples.yaml --maxEvents -1
```

```bash
failed jobs submitted
#SBATCH --array=2109,2110,2115,2116,2117,2119,2120,2121,2125,2127,2128,2130,2131,2132,2133,2134,2136,2145,2147,2148,2149,2150,2153,2155,2156,2158,2160,2161,2168,2171,2174,2175,2179,2182,2183,2184,2192,2859,2867,2868,2869,2870,2871,2873,2874,2875,2877,2878,2879,2883,2887,2890,2891,2892,2893,2897,2904,2905,2983,2986,2987,2989,2992,2993,2998,3002,3004,3009,3010,3012,3014                    # Total 10784
```
