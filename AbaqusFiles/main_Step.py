from abaqus import *
from abaqusConstants import *

from ModelModule import MyModel

class StepModule(MyModel):

    def createStep(self,stepName='Step-1',previousStep='Initial'):
        mdb.models[MyModel._modelName].ExplicitDynamicsStep(name='Step-1', 
            previous='Initial')
        mdb.models[MyModel._modelName].fieldOutputRequests['F-Output-1'].setValues(
            variables=('S', 'SVAVG', 'PE', 'PEVAVG', 'PEEQ', 'PEEQVAVG', 'LE', 'U', 
            'V', 'A', 'RF', 'CSTRESS', 'DAMAGEC', 'DAMAGET', 'SDEG', 'EVF', 'STATUS'))
        mdb.models[MyModel._modelName].fieldOutputRequests['F-Output-1'].setValues(
            numIntervals=50)
