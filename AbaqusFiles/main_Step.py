from abaqus import *
from abaqusConstants import *

def createStep(stepName,previousStep):
    mdb.models['Model-1'].ExplicitDynamicsStep(name=stepName, previous=previousStep)