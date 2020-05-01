from abaqus import *
from abaqusConstants import *

from ModelModule import MyModel

class StepModule(MyModel):

    def createStep(self,stepName='Step-1',previousStep='Initial'):
        mdb.models[MyModel._modelName].ExplicitDynamicsStep(name=stepName, previous=previousStep)
