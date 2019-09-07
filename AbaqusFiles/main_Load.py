from abaqus import *
from abaqusConstants import *



def setPressureLoad(InstanceName,load,order):
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

        edges2 = e1.findAt(((75,150, 0.0), ))
        region2 = a.Set(edges=edges2, name='Set-'+str(order+1))
        mdb.models['Model-1'].DisplacementBC(name='BC-'+str(order+1), createStepName='Initial', 
                region=region2, u1=SET, u2=UNSET, ur3=UNSET, amplitude=UNSET, 
                distributionType=UNIFORM, fieldName='', localCsys=None)

def setReferConLoad(load,order,id):
        a = mdb.models['Model-1'].rootAssembly
        r1 = a.referencePoints
        refPoints1=(r1[id], )
        region1=a.Set(referencePoints=refPoints1, name='m_Set-Load'+str(order))
        a = mdb.models['Model-1'].rootAssembly
        s1 = a.instances['MainPart'].edges
        side1Edges1 = s1.findAt(((37.5, 150.0, 0.0), ))
        region2=a.Surface(side1Edges=side1Edges1, name='s_Surf-Load'+str(order))
        mdb.models['Model-1'].Coupling(name='Constraint-Load'+str(order), controlPoint=region1, 
        surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC, 
        localCsys=None, u1=ON, u2=ON, ur3=ON)

        a = mdb.models['Model-1'].rootAssembly
        r1 = a.referencePoints
        refPoints1=(r1[id], )
        region = a.Set(referencePoints=refPoints1, name='Set-Load'+str(order))
        mdb.models['Model-1'].ConcentratedForce(name='Load-'+str(order), createStepName='Step-'+str(order), 
        region=region, cf2=load, distributionType=UNIFORM, field='', 
        localCsys=None)

def setReferPoint():
        a = mdb.models['Model-1'].rootAssembly
        e1 = a.instances['MainPart'].edges
        r=a.ReferencePoint(point=a.instances['MainPart'].InterestingPoint(edge=e1.findAt(
        coordinates=(37.5, 150.0, 0.0)), rule=MIDDLE))
        return r.id

def setDspLoad(partName,dsp,order):
        a = mdb.models['Model-1'].rootAssembly
        e1 = a.instances[partName].edges
        edges1 = e1.findAt(((37.5, 150.0, 0.0), ))
        region = a.Set(edges=edges1, name='Set-BC-Load-'+str(order))
        mdb.models['Model-1'].DisplacementBC(name='BC-Load-'+str(order), createStepName='Step-'+str(order), 
        region=region, u1=UNSET, u2=dsp, ur3=UNSET, amplitude=UNSET, fixed=OFF, 
        distributionType=UNIFORM, fieldName='', localCsys=None)
        mdb.models['Model-1'].boundaryConditions['BC-Load-'+str(order)].deactivate('Step-'+str(order+1))


def setReferDspLoad(partName,dsp,order,id):
        a = mdb.models['Model-1'].rootAssembly
        r1 = a.referencePoints
        refPoints1=(r1[id], )
        region1=a.Set(referencePoints=refPoints1, name='m_Set-Load'+str(order))
        a = mdb.models['Model-1'].rootAssembly
        s1 = a.instances[partName].edges
        side1Edges1 = s1.findAt(((37.5, 150.0, 0.0), ))
        region2=a.Surface(side1Edges=side1Edges1, name='s_Surf-Load'+str(order))
        mdb.models['Model-1'].Coupling(name='Constraint-Load'+str(order), controlPoint=region1, 
        surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC, 
        localCsys=None, u1=ON, u2=ON, ur3=ON)

        a = mdb.models['Model-1'].rootAssembly
        r1 = a.referencePoints
        refPoints1=(r1[id], )
        region = a.Set(referencePoints=refPoints1, name='Set-Load'+str(order))
        mdb.models['Model-1'].TabularAmplitude(name='Amp-1', timeSpan=STEP, smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (1.0, 1.0)))
        mdb.models['Model-1'].DisplacementBC(name='BC-Load-'+str(order), createStepName='Step-'+str(order), 
        region=region, u1=UNSET, u2=dsp, ur3=UNSET, amplitude='Amp-1', fixed=OFF, 
        distributionType=UNIFORM, fieldName='', localCsys=None)
        try:
                mdb.models['Model-1'].boundaryConditions['BC-Load-'+str(order)].deactivate('Step-'+str(order+1))
        except:
                pass



