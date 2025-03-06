# Setup conda and fetch python3 environment
source /etc/profile.d/modules.sh
module --force purge
module load conda/2024.09
conda activate /depot/cms/kernels/python3

# Setup VOMS proxy
voms-proxy-init --voms cms --valid 192:00 --out $(pwd)/voms_proxy.txt
export X509_USER_PROXY=$(pwd)/voms_proxy.txt
export XRD_REQUESTTIMEOUT=2400

# Setup CMSSW environment & related commands
source /cvmfs/cms.cern.ch/cmsset_default.sh
