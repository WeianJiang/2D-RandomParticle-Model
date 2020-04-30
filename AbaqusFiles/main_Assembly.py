from abaqus import *
from abaqusConstants import *


def partInst(modelName,partname):
    a = mdb.models[modelName].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models[modelName].parts[partname]
    a.Instance(name=partname, part=p, dependent=ON)


def partTranslate(modelName,InstanceName,target_x,target_y):
    a = mdb.models[modelName].rootAssembly
    a.translate(instanceList=(InstanceName, ), vector=(target_x,target_y, 0.0))
    #: The instance Part-49 was translated by 500.E-03, 0., 0. with respect to the assembly coordinate system