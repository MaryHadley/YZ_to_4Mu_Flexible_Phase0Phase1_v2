#Usage: 
#python crabCfgSubmitZmuon_MC_2016UL.py (to submit jobs)
# ./multicrab.py (to check jobs) -w <workAreaName> -c <command to launch, e.g. status>
#Credit to Maximilian Heindl and this github repo for idea of how to write this crab cfg: https://github.com/CMSHCALCalib/RadDam/blob/master/HFmonitoring/nTuplizer/ggAnalysis/ggNtuplizer/test/crabConfig_data.py


#also credit to this tool for the multicrab.py file: https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRABClientLibraryAPI#Multicrab_using_the_crabCommand

if __name__ == '__main__':

    


    from CRABAPI.RawCommand import crabCommand
    from httplib import HTTPException

    from CRABClient.UserUtilities import config
    config = config()
    
    from multiprocessing import Process
    
    
    #Common configuration
    
    config.General.workArea     = 'Zmuon_MC_DPS_2016UL'
    config.General.transferLogs = False
#    config.JobType.maxMemoryMB = 5000 #Let's try the default to start and see if it works 
#    config.JobType.maxJobRuntimeMin = 2750 #Let's try the default to start and see if it works 
    config.JobType.pluginName   = 'Analysis' 
    config.JobType.psetName     = 'ZmuonAnalyzer_cfg.py'
    config.JobType.pyCfgParams = ["isMC=True"] #https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile, see pyCfgParams
    config.JobType.allowUndistributedCMSSW = True
#    config.JobType.sendExternalFolder = True #I don't have an CMSSW_BASE/external so I don't think I need this 
    config.Data.inputDBS        = 'global'    #Checked, this is what we need 
    config.Data.splitting       = 'FileBased' 
#    config.Data.lumiMask        = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt' #Use the non AFS one when submitting from LPC' #'/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt' #59.83  fb^-1, see: https://twiki.cern.ch/twiki/bin/viewauth/CMS/DCUserPage#Legacy_Re_Reco_aka_UL2018_datase
    config.Data.unitsPerJob     = 1 #5
#    config.Data.unitsPerJob     = 6
  #  config.Data.totalUnits      = 100 #for testing purposes 
    config.Data.ignoreLocality  = False
    config.Data.publication     = False
    config.Data.allowNonValidInputDataset     = True
    config.Site.storageSite     = 'T3_US_FNALLPC' 
    
    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException, hte:
            print hte.headers
            
    
    
    #Dataset dependent Configuration
    
    
    #SingleMu used at one point to do a quick test of something, obsolete now
    
    # Run2018A SingleMu  
#     config.General.requestName = "SingleMuUL_Run2018A"
#     config.Data.inputDataset = "/SingleMuon/Run2018D-12Nov2019_UL2018-v4/MINIAOD"
#     config.Data.outLFNDirBase = "/store/user/mhadley/Zmuon_DataJobs_SingleMu_UL2018A_proofOfConcept_12Oct2020"
#     p = Process(target=submit, args=(config,))
#     p.start()
#     p.join()

    # Z+Y DPS 2016UL APV
    config.General.requestName = 'ZY_DPS_2016UL' 
    config.Data.inputDataset   = '/DPS_ToZY_ZToMuMu_YToMuMu_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAOD-106X_mcRun2_asymptotic_v13-v1/MINIAODSIM' 
    config.Data.outLFNDirBase  = '/store/user/mhadley/Zmuon_MC_DPS_2016UL_ZY'
    p = Process(target=submit, args=(config,))
    p.start()
    p.join()
    
    # Y+Z DPS 2016UL APV
    config.General.requestName = 'YZ_DPS_2016UL' 
    config.Data.inputDataset   = '/DPS_ToYZ_YToMuMu_ZToMuMu_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAOD-106X_mcRun2_asymptotic_v13-v1/MINIAODSIM' 
    config.Data.outLFNDirBase  = '/store/user/mhadley/Zmuon_MC_DPS_2016UL_YZ'
    p = Process(target=submit, args=(config,))
    p.start()
    p.join()

    

