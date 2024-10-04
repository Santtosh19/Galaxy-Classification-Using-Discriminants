from scripts.helperFuncs import *

# command line arguments and basic settings
# --------------------------------------------------------------------------------------------------
init()

# just in case... (may comment this out)
if not glob.annz["doSingleCls"]:
  log.info(red(" - "+time.strftime("%d/%m/%y %H:%M:%S")+" - This scripts is only designed for singleClassification...")) ; sys.exit(0)

# ==================================================================================================
# The main code - single classification -
# --------------------------------------------------------------------------------------------------
#   - run the following:
#     python annz_singleCls.py --singleClassification --genInputTrees
#     python annz_singleCls.py --singleClassification --train
#     python annz_singleCls.py --singleClassification --optimize
#     python annz_singleCls.py --singleClassification --evaluate
# --------------------------------------------------------------------------------------------------
log.info(whtOnBlck(" - "+time.strftime("%d/%m/%y %H:%M:%S")+" - starting ANNZ"))

# --------------------------------------------------------------------------------------------------
# general options which are the same for all stages
#   - PLEASE ALSO INSPECT generalSettings(), WHICH HAS BEEN RUN AS PART OF init(), FOR MORE OPTIONS
# --------------------------------------------------------------------------------------------------
# outDirName - set output directory name
glob.annz["outDirName"]   = "skyserver10"

# nMLMs - the number of random MLMs to generate - for single classification, this must be [1]
glob.annz["nMLMs"]        = 1
glob.annz["minObjTrainTest"]=1
#defSigBckCuts = 1
# the definition of signal and background classes
glob.annz["inpFiles_sig"] = "TRAINboxyDR8_santtosh.csv;TESTboxyDR8_santtosh.csv;EVALboxyDR8_santtosh.csv";
glob.annz["inpFiles_bck"] = "TRAINnobulgeDR8_santtosh.csv;TESTnobulgeDR8_santtosh.csv;TRAINroundedDR8_santtosh.csv;TESTroundedDR8_santtosh.csv;EVALnobulgeDR8_santtosh.csv;EVALroundedDR8_santtosh.csv";
#glob.annz["userCuts_sig"] = "type == 1" 
#glob.annz["userCuts_bck"] = "type == 0"
##############################
### MLM OPTIONS (CHANGE 2) ###
##############################
# Select/edit your MLM options. comment out those that you don't want to use.
########
## RC ##
## Rectangular Cuts. Doesn't work, only gives 0.5 as results.
# mlm_options = "ANNZ_MLM=CUTS: VarTransform=P: FitMethod=GA: EffMethod=EffSel: CutRangeMin=-1: CutRangeMax=-1: VarProp=NotEnforced"

#########
## PLE ##
## Projective Likelihood Estimator. Gives output with accuracy less than 50%.
# mlm_options = "ANNZ_MLM=Likelihood: VarTransform=P: TransformOutput=False"

#########
## KNN ##
## ScaleFrac: does best between 0.1 and 0.9, definitely not 0 or 1.
## nkNN     : depends on size of training sample: = trainsize/5000 for MGS, trainsize/1000 for LRG.
# mlm_options = "ANNZ_MLM=KNN: VarTransform=P: nkNN=100: ScaleFrac=0.9: Kernel=Poln"

############
## PDE-RS ##
## MaxIterations : 1 iteration for every 50 training objects;
## NEventsMin    = 4x^4 - 39x^3 + 128x^2 - 148x + 80, where x is the sample size/50000
## NEventsMax    = NEventsMin + 10
# mlm_options = "ANNZ_MLM=PDERS: VarTransform=P: NEventsMin=100: NEventsMax=200: MaxVIterations=500"

##############
## PDE-FOAM ##
## Probability Density Estimation - FOAM is slower than PDE-RS if you use the following optimised settings. Also don't recommend.
#mlm_options = "ANNZ_MLM=PDEFOAM: VarTransform=P: VolFrac=0.0833: nActiveCells=4000: nSampl=2000: Kernel=Gauss"
num_input=10
#########
## ANN ##
## My trusted machine learning method. There are several ways to select your number of hidden layers, replace h1-5 in the code.
#h1 = str(int(2*num_input))+","+str(int(2*num_input))                             # 2N:2N (ANNz1 default)
h2 = str(int(round((2*num_input+1)/3,0)))+","+str(int(round((num_input+2)/3,0))) # (2N+1)/3:(N+2)/3 (John's default)
#h3 = str(int(round(1.5*num_input,0)))+","+str(int(num_input))                    # 3N/2:N (ANNz2 default)
#h4 = str(int(num_input))+","+str(int(num_input))                                 # N:N
#h5 = str(int(2*num_input))+","+str(int(round(1.5*num_input,0)))                  # 2N:3N/2
mlm_options = "ANNZ_MLM=ANN: VarTransform=D: TrainingMethod=BFGS: SamplingTraining=False: NeuronType=tanh: UseRegulator=False: HiddenLayers="+h2+":RandomSeed=101979"

#########
## BDT ##
#mlm_options = "ANNZ_MLM=BDT: VarTransform=N,P: NTrees=500: BoostType=Bagging: BaggedSampleFraction=1.0: nCuts=20: MinNodeSize=0.02"

#########
##H-MATRIX DISCRIMINANT##
#mlm_options= "ANNZ_MLM=HMatrix: VarTransform=G"

#########
##FISHER DICRIMINANTS##
#mlm_options= "ANNZ_MLM=Fisher: VarTransform=N,P: method=Mahalanobis"

#########
##LINEAR DISCRIMINANT ANALYSIS##
#mlm_options= "ANNZ_MLM=LD: VarTransform=N,P"

#########
##FUNCTION DISCRIMINANT ANALYSIS (FDA)##
#mlm_options= "ANNZ_MLM=FDA: VarTransform=None: Formula=(0)+(1)*x1+(2)*x2+(3)*x3+(4)*x4+(5)*x5+(6)*x6+(7)*x7+(8)*x8+(9)*x9+(10)*x10: ParRanges=(-1,1);(-10,10);(-10,10);(-10,10);(-10,10);(-10,10);(-10,10);(-10,10);(-10,10);(-10,10);(-10,10): FitMethod=MINUIT: Converger=MINUIT" ##for now i keep getting invalid pointers

##################################################################################################################################

# --------------------------------------------------------------------------------------------------
# pre-processing of the input dataset
# --------------------------------------------------------------------------------------------------
if glob.annz["doGenInputTrees"]:
  # inDirName    - directory in which input files are stored
  glob.annz["inDirName"]    = "examples/data/sansaza2/train"

  # inAsciiVars  - list of parameter types and parameter names, corresponding to columns in the input
  #                file, e.g., [TYPE:NAME] may be [F:MAG_U], with 'F' standing for float. (see advanced example for detailed explanation)
  glob.annz["inAsciiVars"]  = "F: objid; I: type; F: dered_g;F: dered_r; F: dered_i; F: deVAB_i; F: expAB_i; F: lnLexp_i; F: lnLdeV_i; " \
                            + " F: lnLstar_i; F: petroR90_i; F: petroR50_i; F: mRrCc_i; F: mCr4_i"

  # --------------------------------------------------------------------------------------------------
  # - inAsciiFiles - list of files for training, testing and validation. objects are selected for each subsample from the entire
  #                  dataset.
  # - splitType    - deteermine the method for splitting the dataset into trainig testing and validation subsamples.
  # - see e.g., annz_rndReg_advanced.py for alternative ways to define input files and split datasets
  # --------------------------------------------------------------------------------------------------
  #glob.annz["splitType"]    = "serial" # "serial", "blocks" or "random"
  #glob.annz["inAsciiFiles"] = "sgCatalogue_galaxy_0.txt;sgCatalogue_galaxy_1.txt;sgCatalogue_star_0.txt;sgCatalogue_star_1.txt;sgCatalogue_star_3.txt"
  glob.annz["splitType"]      = "byInFiles"
  glob.annz["splitTypeTrain"] = "TRAINboxyDR8_santtosh.csv;TRAINnobulgeDR8_santtosh.csv;TRAINroundedDR8_santtosh.csv"
  #TRAINnobulgeDR8_santtosh.csv;TRAINroundedDR8_santtosh.csv"
  glob.annz["splitTypeTest"]  = "TESTboxyDR8_santtosh.csv;TESTnobulgeDR8_santtosh.csv;TESTroundedDR8_santtosh.csv"
  #train ="TRAINboxyRD8_santtosh.csv;TRAINnobulgeRD8_santtosh.csv;TRAINroundedRD8_santtosh.csv"
  #test="TESTboxyRD8_santtosh.csv;TESTnobulgeRD8_santtosh.csv;TESTroundedRD8_santtosh.csv"
  #valid="VALIDnobulgeRD8_santtosh.csv;VALIDroundedRD8_santtosh.csv"
  # run ANNZ with the current settings
  runANNZ()

# --------------------------------------------------------------------------------------------------
# training
# --------------------------------------------------------------------------------------------------
if glob.annz["doTrain"]:
  # for each MLM, run ANNZ
  for nMLMnow in range(glob.annz["nMLMs"]): 
    glob.annz["nMLMnow"] = nMLMnow
    if glob.annz["trainIndex"] >= 0 and glob.annz["trainIndex"] != nMLMnow: continue

    # rndOptTypes - generate these randomized MLM types (currently "ANN", "BDT" or "ANN_BDT" are supported).
    #glob.annz["rndOptTypes"] = "BDT" # for this example, since BDTs are much faster to train, exclude ANNs...
    glob.annz["doMultiCls"] = True
    # inputVariables - semicolon-separated list of input variables for the MLMs. Can include math expressions of the variables
    # given in inAsciiVars (see https://root.cern.ch/root/html520/TFormula.html for examples of valid math expressions)
    glob.annz["inputVariables"]    = "deVAB_i; expAB_i; lnLexp_i; lnLdeV_i; " \
                            + " lnLstar_i; mRrCc_i; mCr4_i; petroR90_i/petroR50_i; dered_g-dered_r; dered_r-dered_i" 
    #i can put different types of MLM here
    glob.annz["userMLMopts"] = mlm_options
    
    
    # can place here specific randomization settings, cuts and weights (see advanced example for details)
    glob.annz["ANNZ_nTrain_sig"]="nTrainSig*281"
    #glob.annz["userWeights_train"]="inpFiles_sig*281"
    #glob.annz["userWeights_valid"]="inpFiles_sig*281"
    #glob.annz["userWeights_train"] = "deVAB_i*281; expAB_i*281; lnLexp_i*281; lnLdeV_i*281; " \
                            #+ " lnLstar_i*281; mRrCc_i*281; mCr4_i*281; (petroR90_i/petroR50_i)*281; (dered_g-dered_r)*281; (dered_r-dered_i)*281"
    #glob.annz["userWeights_valid"] = "deVAB_i*281; expAB_i*281; lnLexp_i*281; lnLdeV_i*281; " \
                           # + " lnLstar_i*281; mRrCc_i*281; mCr4_i*281; (petroR90_i/petroR50_i)*281; (dered_g-dered_r)*281; (dered_r-dered_i)*281"
    # if this is left as is, then random job options are generated internally in ANNZ, using MLM types
    # given by rndOptTypes. see ANNZ::generateOptsMLM().
    
    
    # ....
    # --------------------------------------------------------------------------------------------------

    # run ANNZ with the current settings
    runANNZ()

# --------------------------------------------------------------------------------------------------
# optimization and evaluation
# --------------------------------------------------------------------------------------------------
if glob.annz["doOptim"] or glob.annz["doEval"]:

  # --------------------------------------------------------------------------------------------------
  # optimization
  # --------------------------------------------------------------------------------------------------
  if glob.annz["doOptim"]:
    # run ANNZ with the current settings
    runANNZ()

  # --------------------------------------------------------------------------------------------------
  # evaluation
  # --------------------------------------------------------------------------------------------------
  if glob.annz["doEval"]:

    # inDirName,inAsciiFiles - directory with files to make the calculations from, and list of input files
    glob.annz["inDirName"]    = "examples/data/sansaza2/eval/"
    glob.annz["inAsciiFiles"] = "EVALboxyDR8_santtosh.csv;EVALnobulgeDR8_santtosh.csv;EVALroundedDR8_santtosh.csv"
    # inAsciiVars - list of parameters in the input files (doesnt need to be exactly the same as in doGenInputTrees, but must contain all
    #               of the parameers which were used for training)
    glob.annz["inAsciiVars"]  =  "F: objid; I: type; F: dered_g;F: dered_r; F: dered_i; F: deVAB_i; F: expAB_i; F: lnLexp_i; F: lnLdeV_i; " \
                            + " F: lnLstar_i; F: petroR90_i; F: petroR50_i; F: mRrCc_i; F: mCr4_i"
    #                  (can be used to prevent multiple evaluation of different input files from overwriting each other)
    glob.annz["evalDirPostfix"] = ""
    
    ##santtosh addition: adding the input variables as output var on the csv file
    glob.annz["addOutputVars"] = "type"

    # run ANNZ with the current settings
    runANNZ()

log.info(whtOnBlck(" - "+time.strftime("%d/%m/%y %H:%M:%S")+" - finished running ANNZ !"))

'''
python examples/scripts/sansazacls2.py --singleClassification --genInputTrees
python examples/scripts/sansazacls2.py --singleClassification --train
python examples/scripts/sansazacls2.py --singleClassification --optimize
python examples/scripts/sansazacls2.py --singleClassification --evaluate
'''



