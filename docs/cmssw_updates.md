# nanoAOD customizations

- Link to the cmssw branch that contains the update: [https://github.com/ram1123/cmssw/commits/CMSSW_10_6_30_HHWWgg_nanoV9](https://github.com/ram1123/cmssw/commits/CMSSW_10_6_30_HHWWgg_nanoV9)
    - Branch name: `CMSSW_10_6_30_HHWWgg_nanoV9`

## Changes in the cmssw config file

1. Added the additional variables for the photons
    - some help from changes done by `tautuaGammaGamma` group. Link: [https://github.com/fsetti/privateMC_gen/blob/dd1f731d793c11842f153d630f1f55fc8f55b2f5/no_fixedGridRho_CMSSW/package.tar.gz](https://github.com/fsetti/privateMC_gen/blob/dd1f731d793c11842f153d630f1f55fc8f55b2f5/no_fixedGridRho_CMSSW/package.tar.gz)
        - The above link is from GitHub repository:  [https://github.com/ram1123/privateMC_gen_tautauGammaGamma](https://github.com/ram1123/privateMC_gen_tautauGammaGamma)
            - Branch: `private_nanoaod_production`
    - Other variables:
        - Add the rho variable "fixedGridRhoAll", which was used in Run2 Hgg analyses in flashgg:  https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/NanoAOD/python/globals_cff.py#L24
            - This rho used to correct the pfphotoniso in the preselection: https://github.com/cms-analysis/flashgg/blob/dev_legacy_runII/Taggers/python/flashggPreselectedDiPhotons_cfi.py#L67
        - Add the supercluster eta, superCluster().eta().
            - Although we can estimate the SC eta from eta with the codes shared by Swagata [https://twiki.cern.ch/twiki/pub/CMS/EgammaNanoAOD/scEtaPhoNanoAOD.C](https://twiki.cern.ch/twiki/pub/CMS/EgammaNanoAOD/scEtaPhoNanoAOD.C), it’s not a precise estimation.
                - For details, one can check the comparison on S5 from Junquan's presentation [https://indico.cern.ch/event/1233738/contributions/5474144/attachments/2675923/4640510/2023_LMComparions_UL18_Hgg.pdf](https://indico.cern.ch/event/1233738/contributions/5474144/attachments/2675923/4640510/2023_LMComparions_UL18_Hgg.pdf). The max difference between the estimated SC eta and the real SC eta can be higher to `~0.005``. it’s large compared to precision of the SC eta selection for EB, `<1.4442` (4 digits after the decimal). The photon super cluster eta, not the photon eta, should be used in the analysis for many cases, such as the preselection [flashggPreselectedDiPhotons_cfi.py#L73](https://github.com/cms-analysis/flashgg/blob/dev_legacy_runII/Taggers/python/flashggPreselectedDiPhotons_cfi.py#L73) and the systematics (eta boundaries, for example [flashggDiPhotonSystematics2018_Legacy_cfi.py#L373](https://github.com/cms-analysis/flashgg/blob/dev_legacy_runII/Systematics/python/flashggDiPhotonSystematics2018_Legacy_cfi.py#L373)).

2. Added particleTransformer scores for the HWW tagging:
    - Reference:
        1. https://github.com/gqlcms/Customized_NanoAOD
        2. https://github.com/ZhenxuanZhang-Jensen/Customized_NanoAOD
