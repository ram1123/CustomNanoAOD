from CRABClient.UserUtilities import config
config = config()

config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False
config.General.requestName = "test"

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PPD-RunIISummer20UL18_NanoAODv12_cfg_crab.py'
config.JobType.maxMemoryMB = 3000
config.JobType.numCores = 1
# config.JobType.inputFiles = task.getFilesToTransfer()
config.JobType.disableAutomaticOutputCollection = True
# config.JobType.pyCfgParams = task.getParams()
# config.JobType.maxJobRuntimeMin = task.getMaxJobRuntime() * 60 - 1

config.Data.inputDBS = 'global'
# config.Data.allowNonValidInputDataset = task.allowNonValid
config.Data.publication = False
config.Data.unitsPerJob = 10
config.Data.splitting = 'FileBased'
# config.Data.lumiMask = task.getLumiMask()
config.Data.inputDataset = '/DYJetsToMuMu_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM'
# config.Data.inputDataset = task.inputDataset
# config.Data.ignoreLocality = task.getIgnoreLocality()

config.Data.outLFNDirBase = '/store/user/rasharma/custom_nanoAOD/NanoAODv12/'
config.Data.outputDatasetTag = 'RunIISummer20UL18NanoAODv12'

config.Site.storageSite = 'T2_US_Purdue'
