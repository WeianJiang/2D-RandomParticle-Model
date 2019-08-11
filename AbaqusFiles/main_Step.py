from abaqus import *
from abaqusConstants import *

def createStep(stepName,previousStep):
    mdb.models['Model-1'].StaticStep(name=stepName, previous=previousStep)