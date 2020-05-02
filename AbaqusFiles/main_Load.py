from abaqus import *
from abaqusConstants import *

from ModelModule import MyModel

class LoadModule(MyModel):

        def _createAMP(self):
                mdb.models[MyModel._modelName].SmoothStepAmplitude(name='SmooothStepAMP', timeSpan=STEP, 
                data=((0.0, 0.0), (1.0, 1.0)))

        # def setPressureLoad(self,InstanceName,load,size,order):
        #         a = mdb.models[MyModel._modelName].rootAssembly
        #         s1 = a.instances[InstanceName].edges
        #         side1Edges1 = s1.findAt(((size/2, size, 0.0), ))
        #         region = a.Surface(side1Edges=side1Edges1, name='Surf-'+str(order))
        #         mdb.models[MyModel._modelName].Pressure(name='Load-'+str(order), createStepName='Step-'+str(order), 
        #                 region=region, distributionType=UNIFORM, field='', magnitude=load, amplitude=UNSET)


        def setBoundary(self,order):
                a = mdb.models[MyModel._modelName].rootAssembly
                e1 = a.instances[MyModel._concretePartName].edges
                edges1 = e1.findAt(((MyModel._sectionLength/2,0, 0.0), ))
                region = a.Set(edges=edges1, name='Set-'+str(order))
                mdb.models[MyModel._modelName].DisplacementBC(name='BC-'+str(order), createStepName='Initial', 
                region=region, u1=UNSET, u2=SET, ur3=UNSET, amplitude=UNSET, 
                distributionType=UNIFORM, fieldName='', localCsys=None)

                # edges2 = e1.findAt(((75,size, 0.0), ))
                # region2 = a.Set(edges=edges2, name='Set-'+str(order+1))
                # mdb.models[MyModel._modelName].DisplacementBC(name='BC-'+str(order+1), createStepName='Initial', 
                #         region=region2, u1=SET, u2=UNSET, ur3=UNSET, amplitude=UNSET, 
                #         distributionType=UNIFORM, fieldName='', localCsys=None)

        def setReferConLoad(self,load,order,id):
                a = mdb.models[MyModel._modelName].rootAssembly
                r1 = a.referencePoints
                refPoints1=(r1[id], )
                region1=a.Set(referencePoints=refPoints1, name='m_Set-Load'+str(order))
                a = mdb.models[MyModel._modelName].rootAssembly
                s1 = a.instances['MainPart'].edges
                side1Edges1 = s1.findAt(((37.5, MyModel._sectionHeight, 0.0), ))
                region2=a.Surface(side1Edges=side1Edges1, name='s_Surf-Load'+str(order))
                mdb.models[MyModel._modelName].Coupling(name='Constraint-Load'+str(order), controlPoint=region1, 
                surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC, 
                localCsys=None, u1=ON, u2=ON, ur3=ON)

                a = mdb.models[MyModel._modelName].rootAssembly
                r1 = a.referencePoints
                refPoints1=(r1[id], )
                region = a.Set(referencePoints=refPoints1, name='Set-Load'+str(order))
                mdb.models[MyModel._modelName].ConcentratedForce(name='Load-'+str(order), createStepName='Step-'+str(order), 
                region=region, cf2=load, distributionType=UNIFORM, field='', 
                localCsys=None)

        def setReferPoint(self):
                a = mdb.models[MyModel._modelName].rootAssembly
                e1 = a.instances[MyModel._concretePartName].edges
                r=a.ReferencePoint(point=a.instances[MyModel._concretePartName].InterestingPoint(edge=e1.findAt(
                coordinates=(37.5, MyModel._sectionHeight, 0.0)), rule=MIDDLE))
                return r.id

        # def setDspLoad(self,partName,dsp,size,order):
        #         a = mdb.models[MyModel._modelName].rootAssembly
        #         e1 = a.instances[partName].edges
        #         edges1 = e1.findAt(((37.5, size, 0.0), ))
        #         region = a.Set(edges=edges1, name='Set-BC-Load-'+str(order))
        #         mdb.models[MyModel._modelName].DisplacementBC(name='BC-Load-'+str(order), createStepName='Step-'+str(order), 
        #         region=region, u1=UNSET, u2=dsp, ur3=UNSET, amplitude=UNSET, fixed=OFF, 
        #         distributionType=UNIFORM, fieldName='', localCsys=None)
        #         mdb.models[MyModel._modelName].boundaryConditions['BC-Load-'+str(order)].deactivate('Step-'+str(order+1))


        def setReferDspLoad(self,dsp,order,id):
                a = mdb.models[MyModel._modelName].rootAssembly
                r1 = a.referencePoints
                refPoints1=(r1[id], )
                region1=a.Set(referencePoints=refPoints1, name='m_Set-Load'+str(order))
                a = mdb.models[MyModel._modelName].rootAssembly
                s1 = a.instances[MyModel._concretePartName].edges
                side1Edges1 = s1.findAt(((37.5, MyModel._sectionHeight, 0.0), ))
                region2=a.Surface(side1Edges=side1Edges1, name='s_Surf-Load'+str(order))
                mdb.models[MyModel._modelName].Coupling(name='Constraint-Load'+str(order), controlPoint=region1, 
                surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC, 
                localCsys=None, u1=ON, u2=ON, ur3=ON)

                a = mdb.models[MyModel._modelName].rootAssembly
                r1 = a.referencePoints
                refPoints1=(r1[id], )
                region = a.Set(referencePoints=refPoints1, name='Set-Load'+str(order))
                mdb.models[MyModel._modelName].TabularAmplitude(name='Amp-1', timeSpan=STEP, smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (1.0, 1.0)))
                mdb.models[MyModel._modelName].DisplacementBC(name='BC-Load-'+str(order), createStepName='Step-'+str(order), 
                region=region, u1=UNSET, u2=dsp, ur3=UNSET, amplitude='Amp-1', fixed=OFF, 
                distributionType=UNIFORM, fieldName='', localCsys=None)
                try:
                        mdb.models[MyModel._modelName].boundaryConditions['BC-Load-'+str(order)].deactivate('Step-'+str(order+1))
                except:
                        pass



