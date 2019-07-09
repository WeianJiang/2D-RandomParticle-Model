from abaqus import *
from abaqusConstants import *


def partInst(partname):
    a = mdb.models['Model-1'].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-1'].parts[partname]
    a.Instance(name=partname, part=p, dependent=ON)


def partTranslate(InstanceName,target_x,target_y):
    a = mdb.models['Model-1'].rootAssembly
    a.translate(instanceList=(InstanceName, ), vector=(target_x,target_y, 0.0))
    #: The instance Part-49 was translated by 500.E-03, 0., 0. with respect to the assembly coordinate system