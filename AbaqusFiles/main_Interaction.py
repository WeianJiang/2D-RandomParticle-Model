from abaqus import *
from abaqusConstants import *
import interaction

from ModelModule import MyModel

class InteractionModule(MyModel):


    def createRoughIntrcnzProperty(self):

        mdb.models[MyModel._modelName].ContactProperty('RoughContact')
        mdb.models[MyModel._modelName].interactionProperties['RoughContact'].TangentialBehavior(
            formulation=ROUGH)

    def createInteration(self):
        # the upper plate 
        a = mdb.models[MyModel._modelName].rootAssembly
        s1 = a.instances['UpperPlate'].edges
        side2Edges1 = s1.findAt(((MyModel._sectionLength/2, MyModel._sectionHeight, 0.0), ))
        region1=a.Surface(side2Edges=side2Edges1, name='UpperPlateSurface')

        a = mdb.models[MyModel._modelName].rootAssembly
        s1 = a.instances[MyModel._concretePartName].edges
        side1Edges1 = s1.findAt(((MyModel._sectionLength/2, MyModel._sectionHeight, 0.0), ))
        region2=a.Surface(side1Edges=side1Edges1, name='UpperInstanceSurface')

        mdb.models[MyModel._modelName].SurfaceToSurfaceContactExp(name ='Upper-Interaction', 
            createStepName='Step-1', master = region1, slave = region2, 
            mechanicalConstraint=PENALTY, sliding=FINITE, 
            interactionProperty='RoughContact', initialClearance=OMIT, datumAxis=None, 
            clearanceRegion=None)

        #the lower plate
        a = mdb.models[MyModel._modelName].rootAssembly
        s1 = a.instances['LowerPlate'].edges
        side1Edges1 = s1.findAt(((MyModel._sectionLength/2, 0, 0.0), ))
        region1=a.Surface(side1Edges=side1Edges1, name='LowerPlateSurface')

        a = mdb.models[MyModel._modelName].rootAssembly
        s1 = a.instances[MyModel._concretePartName].edges
        side1Edges1 = s1.findAt(((MyModel._sectionLength/2, 0, 0.0), ))
        region2=a.Surface(side1Edges=side1Edges1, name='LowerInstanceSurface')
        mdb.models[MyModel._modelName].SurfaceToSurfaceContactExp(name ='Lower-Interaction', 
            createStepName='Step-1', master = region1, slave = region2, 
            mechanicalConstraint=PENALTY, sliding=FINITE, 
            interactionProperty='RoughContact', initialClearance=OMIT, datumAxis=None, 
            clearanceRegion=None)

    def createRigidBody(self,RefID,InstanceName):
        '''
        InstanceName='UpperPlate' or 'LowerPlate'
        '''
        a = mdb.models[MyModel._modelName].rootAssembly

        if InstanceName=='UpperPlate':
            height=MyModel._sectionHeight
        elif InstanceName=='LowerPlate':
            height=0

        e1 = a.instances[InstanceName].edges
        edges1 = e1.findAt(((MyModel._sectionLength/2, height, 0.0), ))
        region2=a.Set(edges=edges1, name='Rigid_Set-'+InstanceName)

        r1 = a.referencePoints
        refPoints1=(r1[RefID], )
        import regionToolset
        region1=regionToolset.Region(referencePoints=refPoints1)

        mdb.models[MyModel._modelName].RigidBody(name=InstanceName+'RigidBody', 
        refPointRegion=region1, bodyRegion=region2, refPointAtCOM=ON)

    # def creatingTie(modelName,MasterinstanceName,SlaveinstanceName,target_x,target_y,radi,order):
    #     a = mdb.models[modelName].rootAssembly
    #     s1 = a.instances[MasterinstanceName].edges
    #     side1Edges1 = s1.findAt(((target_x, target_y+radi, 0.0), ))
    #     region1=a.Surface(side1Edges=side1Edges1, name='m_Surf-'+MasterinstanceName+str(order))
    #     a = mdb.models[modelName].rootAssembly
    #     s1 = a.instances[SlaveinstanceName].edges
    #     side1Edges1 = s1.findAt(((target_x, target_y+radi, 0.0), ))
    #     region2=a.Surface(side1Edges=side1Edges1, name='s_Surf-'+SlaveinstanceName+str(order))
    #     mdb.models[modelName].Tie(name='Constraint-'+MasterinstanceName+str(order), master=region1, slave=region2, 
    #         positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)