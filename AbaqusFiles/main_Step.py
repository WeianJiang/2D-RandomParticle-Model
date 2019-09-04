from abaqus import *
from abaqusConstants import *

def createStep(stepName,previousStep):
    #mdb.models['Model-1'].StaticStep(name=stepName, previous=previousStep)
    #mdb.models['Model-1'].StaticStep(name=stepName, previous=previousStep)
    mdb.models['Model-1'].ImplicitDynamicsStep(name=stepName, previous=previousStep, 
    timePeriod=2.0, maxNumInc=100000, initialInc=5e-05, minInc=1e-015, 
    maxInc=0.01)