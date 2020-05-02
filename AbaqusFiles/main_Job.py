from abaqus import *
from abaqusConstants import *

import job

from ModelModule import MyModel

class JobModule(MyModel):

    def createJob(self,name,cpus=1):
        mdb.Job(name=MyModel._modelName, model=MyModel._modelName, description='', type=ANALYSIS, 
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
            scratch='', parallelizationMethodExplicit=DOMAIN, numDomains=cpus, 
            activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=cpus)

    def submitJob(self):
        mdb.jobs[MyModel._modelName].submit(consistencyChecking=OFF)