jdl_part_1 = """Executable = HH_WWgg_Signal_v2.sh
Universe = vanilla
Notification = ERROR
Should_Transfer_Files = YES
Transfer_Output_Files = ""
Transfer_Input_Files = HH_WWgg_Signal_v2.sh, cmssw_modified_config_files/HIG-RunIISummer20UL18NanoAODv9-02546_1_cfg.py, cmssw_modified_config_files/DATA-Run2018-NanoAODv9-02546_1_cfg.py
x509userproxy = $ENV(X509_USER_PROXY)
getenv      = True
+JobFlavour = "tomorrow"
request_memory = 12000
request_cpus = 8
"""

jdl_part_2 = """
Output = logs/UL2018/EGamma_Run2018A/{ResubmitString}_log_$(Cluster)_$(Process).stdout
Error  = logs/UL2018/EGamma_Run2018A/{ResubmitString}_log_$(Cluster)_$(Process).stdout
Log  = logs/UL2018/EGamma_Run2018A/{ResubmitString}_log_$(Cluster)_$(Process).err
Arguments = $(Cluster) $(Process)   DATA-Run2018-NanoAODv9-02546_1_cfg.py {Infile} EGamma_Run2018A_$(Cluster)_$(Process)_{ResubmitString}.root /eos/user/r/rasharma/post_doc_ihep/double-higgs/nanoAODnTuples/nanoAOD_20Oct2023/UL2018/EGamma_Run2018A
Queue 1
"""
