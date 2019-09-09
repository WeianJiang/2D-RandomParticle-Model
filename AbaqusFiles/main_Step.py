from abaqus import *
from abaqusConstants import *

def createStep(modelName,stepName,previousStep):
    #mdb.models['Model-1'].StaticStep(name=stepName, previous=previousStep)
    #mdb.models['Model-1'].StaticStep(name=stepName, previous=previousStep)
    mdb.models[modelName].ImplicitDynamicsStep(name=stepName, previous=previousStep, 
    timePeriod=1.0, maxNumInc=100000, initialInc=5e-05, minInc=1e-015, 
    maxInc=0.01)