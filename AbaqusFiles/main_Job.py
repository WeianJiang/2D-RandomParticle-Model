from abaqus import *
from abaqusConstants import *

import job

def creatJob(name,cpus=1):
    mdb.Job(name=name, model='Model-1', description='',  type=ANALYSIS,
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', multiprocessingMode=DEFAULT, numCpus=cpus, numGPUs=0)
    mdb.jobs[name].submit(consistencyChecking=OFF)