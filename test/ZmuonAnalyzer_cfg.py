import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing #https://twiki.cern.ch/CMSPublic/SWGuideAboutPythonConfigFile#Passing_Command_Line_Arguments_T

process = cms.Process("analysis")

options = VarParsing.VarParsing("analysis")



#List of Options
options.register( "applyZmuonFilter",
    True,
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.bool,
    "Shall we prefilter out some events and never bother giving them to the analyzer? Defaults to True. If you change to false, you will need to, for the moment, comment out the indicated lines in the ZmuonAnalyzer.cc. Will flag with a comment 'If applyZmuonFilter=False, comment out!'"
)

options.register("isMC",
    True, #set to false for crab test run
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.bool,
    "Is this simulation (aka MC) or is it data we have collected from the CMS detector? Defaults to True."
            
)

# options.register("triggerYear",
#                 2018,
#                 VarParsing.VarParsing.multiplicity.singleton,
#                 VarParsing.VarParsing.varType.int,
#                 "Select trigger year to use. Options are 2016, 2017, or 2018. Defaults to 2018."
# 
# )

options.register("isSPS",
    False,
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.bool,
    "Is this single parton scattering (SPS) MC? Make sure you are running on MC! Defaults to False." 
)




# This needs to go here, after we have defined all the options!
options.parseArguments()
print "Options are:", options

process.ZmuonAnalyzer = cms.EDAnalyzer("ZmuonAnalyzer",
   muonCollection = cms.InputTag("slimmedMuons"),
   electronCollection = cms.InputTag("slimmedElectrons"),
   bits = cms.InputTag("TriggerResults","", "HLT"),
   #objects = cms.InputTag("selectedPatTrigger"),
   objects = cms.InputTag("slimmedPatTrigger"), #corrected 11 Oct. 2021, see email from K.P.
   genParticles = cms.InputTag("prunedGenParticles"),
   vertexCollection = cms.InputTag("offlineSlimmedPrimaryVertices"),
   metTag = cms.InputTag("slimmedMETs"),
   pfCands = cms.InputTag("packedPFCandidates"),
   rho     = cms.InputTag("fixedGridRhoFastjetAll"), #Median energy density, see: https://arxiv.org/pdf/0707.1378.pdf
  #Might add Pileup here later if I think it is something we might change ever, but at the moment is hard-coded in the analyzer
   datasets = cms.vstring("SingleMuon", "DoubleMuon"),
   stageL1Trigger = cms.uint32(2),
   isMC   = cms.bool(options.isMC),
   isSPS = cms.bool(options.isSPS),
 #  triggerYear = cms.int32(options.triggerYear),
)

if options.applyZmuonFilter:
   process.ZmuonFilter = cms.EDFilter("ZmuonFilter",
     muonCollection = cms.InputTag("slimmedMuons"),
     bits = cms.InputTag("TriggerResults","", "HLT"),
 #    objects = cms.InputTag("selectedPatTrigger"),
     objects = cms.InputTag("slimmedPatTrigger"),
#     genParticles = cms.InputTag("prunedGenParticles"), #not needed here
#     pfCands = cms.InputTag("packedPFCandidates")  #not needed here
     pTCut = cms.double(0.5), #was 2.
     etaCut = cms.double(3.),
     invMass4MuCut_low = cms.double(50), #usually 50
    #invMass4MuCut_high = cms.double(500.), #this is essentially not doing anything
  )
   process.nEventsTotal = cms.EDProducer("EventCountProducer")
   process.nEventsFiltered = cms.EDProducer("EventCountProducer")

#process.maxEvents.input = 1000

#process.maxEvents = cms.untracked.PSet(
#   input = cms.untracked.int32(40000)
#   input = cms.untracked.int32(-1)
 #  input = cms.untracked.int32(1000) #for crab test, just look at 1000 events

#)


process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#                                          "file:../miniAOD_01.root",
#                                          "file:../miniAOD_02.root",
#                                          "file:../miniAOD_03.root",
#                                          "file:../miniAOD_04.root",
#                                          "file:../miniAOD_05.root",
#                                          "file:../miniAOD_06.root"
#                                          "file:../../../miniAOD_lowStats.root",
#                                           "file:../SingleMu_Run2018A-17Sep2018-v2_F8CDAAA9-11C7-A34F-A059-409CF95EB82A.root",
#                                           "file:../SingleMu_2017B-31Mar2018-v1_FC2B7874-F538-E811-9C29-0025905A60A8.root",
#                                            "file:0079D4A1-71DE-AF4B-90E4-115037F02923.root", #DiMu Run18 A
 #                                             "file:FD881AE8-B6AC-8E4F-9453-2D5E6135D476.root" #DiMu Run18 A
 #                                            "file:E36DDD08-CC3D-6D49-8C71-C6E8C201A2E5.root", #this is DiMU 2018RunB data
 #                                            "file:../YZ_4MuFS_DPS_APV_MiniAOD_2016UL_Yfirst_Zsecond_03_10_2020.root",
 #                                           "file:../YZ_4MuFS_DPS_APV_MiniAOD_2016UL_Zfirst_Ysecond_03_10_2020.root",
#                                           "file:../YZ_4MuFS_DPS_MiniAOD_2016UL_Yfirst_Zsecond_03_10_2020.root",
#                                          "file:../YZ_4MuFS_DPS_MiniAOD_2016UL_Zfirst_Ysecond_03_10_2020.root",
#                                           "file:../YZ_4MuFS_DPS_MiniAOD_2016UL_Yfirst_Zsecond_06_11_2020.root",
#                                            "file:020353D5-EB7E-3A42-928B-64ABB6449999.root",
#                                            "file:../miniAOD_Marys_LHE.root",
                                            #  "file:Y1S3S11_Z_4Mu_HO_SPS_MiniAOD_shortTest_11_June_2021.root",
   #                                         "file:Y2S3S11_Z_4Mu_HO_SPS_MiniAOD.root",
                                           #"file:MC_DPS_2016_YZ_00623223-2B20-AB42-A456-670F9B3875D5.root", 
                                          # "file:MC_DPS_2016_APV_24653D5E-1FF7-274F-A4B8-BB3E4426E612.root",
                                           #"file:MC_DPS_2017_YZ_070452D8-AA0E-7345-B1A4-F5443D1227C1.root",
                                          #"file:MC_DPS_2018_YZ_04A4F969-2F02-F24D-9BA7-2FAB6D708CB6.root",
                                           #'file:14907725-2B14-B245-B076-5B04C5C36D55.root',
      #                                     'file:Y3S3S11_Z_4Mu_HO_SPS_MiniAOD.root',
                                           #'file:Run2018D_testFiles/file1_BB04A3C7-E0C0-EF46-B787-3C6095D1465A.root',
                                           #'file:Run2016F/5994D9C1-4D6A-0844-B47F-B33105292625.root',
                                          # 'file:Run2017B/0D8C151B-9BC1-E648-8959-4110DF702EBF.root',
                                         # '/store/data/Run2017D/DoubleMuon/MINIAOD/09Aug2019_UL2017-v1/260000/04D869DE-CA0D-7D41-A77F-BC71245E2FF4.root', #Call this 2017_File_1
                                           #'/store/data/Run2016G/DoubleMuon/MINIAOD/21Feb2020_UL2016-v1/230000/0494EFE4-63FD-2448-8E9E-D7C2E5C1E1BE.root', #Call this 2016_File_2 #this one was having trouble being read, trying another (see directly below)
                                         # '/store/data/Run2016G/DoubleMuon/MINIAOD/21Feb2020_UL2016-v1/230000/0088A811-11AC-F54A-84F0-F68127844470.root', #Call this 2016_File_1
                                         #'file:RunIISummer16MiniAODv3-ZZTo4L_13TeV_powheg_pythia8-MINIAODSIM-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-100000-42BA2638-E9C6-E811-9BEB-001A649D47FD.root', #call this 2016_ZZto4L_File1
                                         #'file:RunIISummer16MiniAODv3-ZZTo4L_13TeV_powheg_pythia8-MINIAODSIM-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-100000-122F32C7-DD31-1143-96EB-38BC1B7BA376.root',
                                         #'/store/mc/RunIIAutumn18MiniAOD/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15_ext1-v2/10000/0E131CB3-1C94-FD4F-B2AB-50CE71932513.root',
#                                         '/store/mc/RunIIAutumn18MiniAOD/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15_ext1-v2/10000/122F32C7-DD31-1143-96EB-38BC1B7BA376.root',
#                                         '/store/mc/RunIIAutumn18MiniAOD/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15_ext1-v2/10000/3B37145C-6D2E-1B48-B302-8FD416F69731.root',
#                                         '/store/mc/RunIIAutumn18MiniAOD/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15_ext1-v2/10000/4A0828F7-EE50-4240-A7E2-6D1A6E5CA568.root',
#                                         '/store/mc/RunIIAutumn18MiniAOD/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15_ext1-v2/10000/4E82A14A-00E7-2A48-A9A7-C2DE26FE6F7A.root',
#                                         '/store/mc/RunIIAutumn18MiniAOD/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15_ext1-v2/10000/6FC86321-471F-C243-9FBF-EC44750B3604.root',
                                          #2018ZZTo4L_FileList
                                       #    'file:store-mc-RunIIAutumn18MiniAOD-ZZTo4L_TuneCP5_13TeV_powheg_pythia8-MINIAODSIM-102X_upgrade2018_realistic_v15_ext1-v2-10000/0E131CB3-1C94-FD4F-B2AB-50CE71932513.root',
#                                           'file:store-mc-RunIIAutumn18MiniAOD-ZZTo4L_TuneCP5_13TeV_powheg_pythia8-MINIAODSIM-102X_upgrade2018_realistic_v15_ext1-v2-10000/122F32C7-DD31-1143-96EB-38BC1B7BA376.root',
#                                           'file:store-mc-RunIIAutumn18MiniAOD-ZZTo4L_TuneCP5_13TeV_powheg_pythia8-MINIAODSIM-102X_upgrade2018_realistic_v15_ext1-v2-10000/3B37145C-6D2E-1B48-B302-8FD416F69731.root',
#                                           'file:store-mc-RunIIAutumn18MiniAOD-ZZTo4L_TuneCP5_13TeV_powheg_pythia8-MINIAODSIM-102X_upgrade2018_realistic_v15_ext1-v2-10000/4A0828F7-EE50-4240-A7E2-6D1A6E5CA568.root',
#                                           'file:store-mc-RunIIAutumn18MiniAOD-ZZTo4L_TuneCP5_13TeV_powheg_pythia8-MINIAODSIM-102X_upgrade2018_realistic_v15_ext1-v2-10000/4E82A14A-00E7-2A48-A9A7-C2DE26FE6F7A.root', 
#                                           'file:store-mc-RunIIAutumn18MiniAOD-ZZTo4L_TuneCP5_13TeV_powheg_pythia8-MINIAODSIM-102X_upgrade2018_realistic_v15_ext1-v2-10000/6FC86321-471F-C243-9FBF-EC44750B3604.root', 
                                            #2017ZZTo4L_FileList
                                        #      'file:store-mc-RunIIFall17MiniAODv2-ZZTo4L_13TeV_powheg_pythia8-MINIAODSIM-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1-100000/1E1D1DCC-CDCD-E811-95A2-001517B7D750.root',
#                                              'file:store-mc-RunIIFall17MiniAODv2-ZZTo4L_13TeV_powheg_pythia8-MINIAODSIM-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1-100000/428E74D0-A0CD-E811-8BE2-001E6743E34C.root',
#                                              'file:store-mc-RunIIFall17MiniAODv2-ZZTo4L_13TeV_powheg_pythia8-MINIAODSIM-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1-100000/4E253E70-B7CD-E811-B1D6-001E6743E4BE.root',
#                                              'file:store-mc-RunIIFall17MiniAODv2-ZZTo4L_13TeV_powheg_pythia8-MINIAODSIM-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1-100000/74A3DF52-B2CD-E811-99FE-001E6734B0D4.root',
#                                              'file:store-mc-RunIIFall17MiniAODv2-ZZTo4L_13TeV_powheg_pythia8-MINIAODSIM-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1-100000/7AA5896D-BDCD-E811-B85C-001E67461EF4.root',
#                                             #2016ZZTo4L_FileList
                                          #    'file:store-mc-RunIISummer16MiniAODv3-ZZTo4L_13TeV_powheg_pythia8-MINIAODSIM-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-100000/0A064D6A-F0C6-E811-B803-001A649D4815.root',
#                                              'file:store-mc-RunIISummer16MiniAODv3-ZZTo4L_13TeV_powheg_pythia8-MINIAODSIM-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-100000/1C690301-D9C6-E811-A42A-480FCFF4FC90.root',
#                                              'file:store-mc-RunIISummer16MiniAODv3-ZZTo4L_13TeV_powheg_pythia8-MINIAODSIM-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-100000/206968F5-D0C6-E811-8341-001A649D4DF1.root',
#                                              'file:store-mc-RunIISummer16MiniAODv3-ZZTo4L_13TeV_powheg_pythia8-MINIAODSIM-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-100000/28324326-D1C6-E811-99BD-001A649D4F95.root',
#                                              'file:store-mc-RunIISummer16MiniAODv3-ZZTo4L_13TeV_powheg_pythia8-MINIAODSIM-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-100000/340A78A8-EAC6-E811-A0C1-001A649D48A1.root',
                                               #'/store/data/Run2018A/DoubleMuon/MINIAOD/12Nov2019_UL2018-v2/100000/0004C5E1-8BFE-4044-82CB-C0FC878D9C54.root', #file dataset=/DoubleMuon/Run2018A-12Nov2019_UL2018-v2/MINIAOD #Call this 2018 File 1
                                               'file:0004C5E1-8BFE-4044-82CB-C0FC878D9C54.root',
                                             # 'file:07FCA6B1-25BC-1943-BEB8-F4E367BF4AE7_SPS.root',
                                           #  'file:DPS_MC_2018_ZplusY_0620900D-ABE0-A349-A5EA-E8CF5A601E37.root',
                                             #'file:ZplusY_DPS_2018_2623546A-B8A5-7948-9881-83F4EC856E1F.root',
                                             #'file:DPS_ZplusY_2017_20678EC7-FDB1-364D-A443-419F1189A2CE.root',
                                             #'file:ZplusY_DPS_2016APV_4C3553DF-F7CF-E446-979D-A476C93410DC.root',
                                            # 'file:ZplusY_DPS_2016APV_5519AF91-6961-F94A-860A-70377FB86E78.root',
                                            #'file:ZplusY_2016APV_DPS_F2658DCF-4353-8E4A-A928-0A78CE030269.root',
                                            #'file:ZplusY_DPS_2016_2FDBD31E-7BAF-164D-9E9D-5E09114FE20A.root',
                                            # 'file:DPS_ZplusY_2018_442B8D2F-65E3-1C4C-8876-048C9F5D88EA.root',
                                            # 'file:ZplusY_2017_DPS_83417361-C44F-9F4E-969F-F4B22156E170.root',
                                             #'file:ZplusY_2016APV_B3E02D05-E927-C141-A2A1-6AAD3105EEB9.root',
                                             #'file:ZplusY_DPS_2016_F0292CE5-8576-5444-B5A9-B65EA31AEECC.root',
                                              #'file:309AEB14-71FA-CE4B-8EF4-C6741596D4C7.root',
                                              #'file:8EDF7FE4-E99E-114F-844B-A4C4570F68D9.root', #This is the file from here: /store/mc/RunIISummer20UL16MiniAOD/DPS_ToYZ_YToMuMu_ZToMuMu_TuneCP5_13TeV-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v13-v1/280000/8EDF7FE4-E99E-114F-844B-A4C4570F68D9.root 
                                              #It is job 329 from 2016 YZ (nonAPV)
                                              #'file:SPS_Y1SZ_2018_113B04AD-7796-E640-A9A5-9253BC573DE2.root',
                                              #'file:DPS_2016UL_APV_YZ_531790B0-E786-EC4A-843E-FB116EF6BC1A.root', #Job 97
                                               # 'file:DPS_2016UL_APV_ZY_62C0CC1B-D5DF-DD46-8B20-8BD3262A5E0F.root', #Job 19
                                               #'file:DPS_2016UL_APV_ZY_380BF754-5C6A-3C41-B7F2-83456595FAFD.root', #Job 217
                                              # 'file:DPS_2016UL_APV_ZY_A3DCFD19-323A-EE4B-8056-77C114859EF5.root', #Job 237
                                              #'file:DPS_2016UL_APV_ZY_F7DDE0EC-229A-E74C-8718-313F565E2FA2.root', #Job 251
                                   
                                   
                                    ),
   duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)

process.maxEvents = cms.untracked.PSet(
#   input = cms.untracked.int32(40000)
 # input = cms.untracked.int32(500)
# input = cms.untracked.int32(1)
input=cms.untracked.int32(-1)
#input=cms.untracked.int32(1000)
#input = cms.untracked.int32(10)
#input = cms.untracked.int32(2)
#input = cms.untracked.int32(50)
#input = cms.untracked.int32(100)
  #  input = cms.untracked.int32(3000) #for crab test, just look at 1000 events

)

process.TFileService = cms.Service("TFileService",
   #fileName = cms.string("ZYto4Mu_Zto4Mu_pTCut3_Bjorn_20Dec2022_Brux_inputFileIs_DPS_ZplusY_2018_442B8D2F-65E3-1C4C-8876-048C9F5D88EA_wildCard_testCodeFromSam_updateFromMarko_clearTempVecAdded_notPushingBackTriggerFilterInfo.root")
    fileName = cms.string("flatFile_Data2018_test.root")
)

#process.maxEvents.input = 1000
#process.maxEvents = cms.untracked.PSet(
#   input = cms.untracked.int32(40000)
#   input = cms.untracked.int32(-1)
#    input = cms.untracked.int32(1000) #for crab test, just look at 1000 events

#)

process.options = cms.untracked.PSet(
   wantSummary = cms.untracked.bool(True),
#   SkipEvent = cms.untracked.vstring('ProductNotFound')
)


process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1#10000
#process.MessageLogger.cerr.FwkReport.reportEvery = 10000

#process.MessageLogger = cms.Service("MessageLogger",
#                    destinations   = cms.untracked.vstring('messages.txt')
#)

if options.applyZmuonFilter:
    process.p = cms.Path(
         process.nEventsTotal *process.ZmuonFilter *process.nEventsFiltered * process.ZmuonAnalyzer 
        )

else:


    process.p = cms.Path(
        process.ZmuonAnalyzer
)

process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data') #data, all 3 years
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc_pre_vfp') # 2016 pre VFP change MC
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc') #2016 post VFP change MC
#process.GlobalTag = GlobalTag(process.GlobalTag, '106X_mc2017_realistic_v8') # 2017 MC
#process.GlobalTag = GlobalTag(process.GlobalTag, '106X_upgrade2018_realistic_v15_L1v1') #2018 MC
print "GlobalTag = ", str(process.GlobalTag.globaltag).split("'")[1]
