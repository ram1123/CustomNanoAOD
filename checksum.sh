# InputMiniAODFile=/store/data/Run2018C/SingleMuon/MINIAOD/UL2018_MiniAODv2-v2/130000/3DF3944A-36D3-FC41-A7A0-C91A05B79081.root
InputMiniAODFile=/store/data/Run2018A/SingleMuon/MINIAOD/UL2018_MiniAODv2-v3/2530001/AF57A3BB-1E72-5640-8916-DDBB556CB4BC.root

dasgoclient_output=$(dasgoclient --query="file=${InputMiniAODFile}" --json)

echo ${dasgoclient_output}
echo "------------------------------------------------"
# Step -1: Check the adler32 checksum of the input file
adler32_value_das=$(echo ${dasgoclient_output} | grep -o '"adler32":"[^"]*')
echo "adler32 checksum value from dasgoclient: ${adler32_value_das}"
echo "------------------------------------------------"

adler32_value_das_awk=$(echo ${dasgoclient_output} | grep -o '"adler32":"[^"]*' | awk -F ':"' '{print $2}')
echo "adler32 checksum value from dasgoclient: ${adler32_value_das_awk}"
echo "------------------------------------------------"

InputMiniAODFile_xcache=root://xcache.cms.rcac.purdue.edu/${InputMiniAODFile}
InputMiniAODFile_fnal=root://cmsxrootd.fnal.gov/${InputMiniAODFile}
InputMiniAODFile_global=root://cms-xrd-global.cern.ch/${InputMiniAODFile}

# Step -2: Check the adler32 checksum of the input file
adler32_value_store_xcache=$(xrdadler32 ${InputMiniAODFile_xcache} | awk '{print $1}')
echo "adler32 checksum value from xcache: ${adler32_value_store_xcache}"
echo "------------------------------------------------"
# adler32_value_store_fnal=$(xrdadler32 ${InputMiniAODFile_fnal} | awk '{print $1}')
# echo "adler32 checksum value from fnal: ${adler32_value_store_fnal}"
echo "------------------------------------------------"
adler32_value_store_global=$(xrdadler32 ${InputMiniAODFile_global} | awk '{print $1}')
echo "adler32 checksum value from global: ${adler32_value_store_global}"
echo "------------------------------------------------"

# Step -3: Compare the two adler32 checksum values
if [ "$adler32_value_das_awk" == "$adler32_value_store" ]; then
    InputMiniAODFile=${InputMiniAODFile_xcache}
elif [ "$adler32_value_das_awk" == "$adler32_value_store_fnal" ]; then
    InputMiniAODFile=${InputMiniAODFile_fnal}
elif [ "$adler32_value_das_awk" == "$adler32_value_store_global" ]; then
    InputMiniAODFile=${InputMiniAODFile_global}
else
    echo "Checksum values do not match: ${adler32_value_das} != ${adler32_value_store}"
    exit 1
fi
echo "InputMiniAODFile: ${InputMiniAODFile}"
echo "------------------------------------------------"
