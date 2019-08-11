from abaqus import *
from abaqusConstants import *



def setLoad(InstanceName,load,order):
    a = mdb.models['Model-1'].rootAssembly
    s1 = a.instances[InstanceName].edges
    side1Edges1 = s1.findAt(((75, 150, 0.0), ))
    region = a.Surface(side1Edges=side1Edges1, name='Surf-'+str(order))
    mdb.models['Model-1'].Pressure(name='Load-'+str(order), createStepName='Step-'+str(order), 
        region=region, distributionType=UNIFORM, field='', magnitude=load, amplitude=UNSET)


def setBoundary(InstanceName,order):
    a = mdb.models['Model-1'].rootAssembly
    e1 = a.instances[InstanceName].edges
    edges1 = e1.findAt(((75,0, 0.0), ))
    region = a.Set(edges=edges1, name='Set-'+str(order))
    mdb.models['Model-1'].DisplacementBC(name='BC-'+str(order), createStepName='Initial', 
        region=region, u1=SET, u2=SET, ur3=UNSET, amplitude=UNSET, 
        distributionType=UNIFORM, fieldName='', localCsys=None)