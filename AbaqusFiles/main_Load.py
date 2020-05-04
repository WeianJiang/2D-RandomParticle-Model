from abaqus import *
from abaqusConstants import *
from main_Interaction import InteractionModule
from ModelModule import MyModel

class LoadModule(MyModel):


        def _createLoadingPlate(self):
                #create the loading plate
                s = mdb.models[MyModel._modelName].ConstrainedSketch(name='__profile__', 
                sheetSize=200.0)
                plateSize=MyModel._sectionLength+100
                g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
                s.setPrimaryObject(option=STANDALONE)
                s.Line(point1=(-plateSize/2, 0.0), point2=(plateSize/2, 0.0))
                s.HorizontalConstraint(entity=g[2], addUndoState=False)
                p = mdb.models[MyModel._modelName].Part(name='LoadingPlate', 
                dimensionality=TWO_D_PLANAR, type=DISCRETE_RIGID_SURFACE)
                p = mdb.models[MyModel._modelName].parts['LoadingPlate']
                p.BaseWire(sketch=s)
                s.unsetPrimaryObject()
                p = mdb.models[MyModel._modelName].parts['LoadingPlate']
                del mdb.models[MyModel._modelName].sketches['__profile__']

                #assembly 

                a = mdb.models[MyModel._modelName].rootAssembly
                p = mdb.models[MyModel._modelName].parts['LoadingPlate']
                a.Instance(name='UpperPlate', part=p, dependent=ON)

                a = mdb.models[MyModel._modelName].rootAssembly
                p = mdb.models[MyModel._modelName].parts['LoadingPlate']
                a.Instance(name='LowerPlate', part=p, dependent=ON)
                #translation of upper plate
                a1 = mdb.models[MyModel._modelName].rootAssembly
                a1.translate(instanceList=('UpperPlate', ), vector=(MyModel._sectionLength/2, MyModel._sectionHeight, 0.0))
                #translation of lower plate
                a1 = mdb.models[MyModel._modelName].rootAssembly
                a1.translate(instanceList=('LowerPlate', ), vector=(MyModel._sectionLength/2, 0, 0.0))

                #set the reference point
                indexOfUpperPlate=self._setReferPoint('UpperPlate',MyModel._sectionHeight)
                indexOfLowerPlate=self._setReferPoint('LowerPlate',0)

                #set interaction
                theInteraction=InteractionModule()
                theInteraction.createRoughIntrcnzProperty()
                theInteraction.createInteration()

                theInteraction.createRigidBody(indexOfUpperPlate,'UpperPlate')
                theInteraction.createRigidBody(indexOfLowerPlate,'LowerPlate')




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
a = mdb.models['Model-Default'].rootAssembly
r1 = a.referencePoints
refPoints1=(r1[24], )
region = a.Set(referencePoints=refPoints1, name='Set-9')
mdb.models['Model-Default'].DisplacementBC(name='BC-4', 
    createStepName='Initial', region=region, u1=SET, u2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)

                # edges2 = e1.findAt(((75,size, 0.0), ))
                # region2 = a.Set(edges=edges2, name='Set-'+str(order+1))
                # mdb.models[MyModel._modelName].DisplacementBC(name='BC-'+str(order+1), createStepName='Initial', 
                #         region=region2, u1=SET, u2=UNSET, ur3=UNSET, amplitude=UNSET, 
                #         distributionType=UNIFORM, fieldName='', localCsys=None)

        # def setReferConLoad(self,load,order,id):
        #         a = mdb.models[MyModel._modelName].rootAssembly
        #         r1 = a.referencePoints
        #         refPoints1=(r1[id], )
        #         region1=a.Set(referencePoints=refPoints1, name='m_Set-Load'+str(order))
        #         a = mdb.models[MyModel._modelName].rootAssembly
        #         s1 = a.instances['MainPart'].edges
        #         side1Edges1 = s1.findAt(((37.5, MyModel._sectionHeight, 0.0), ))
        #         region2=a.Surface(side1Edges=side1Edges1, name='s_Surf-Load'+str(order))
        #         mdb.models[MyModel._modelName].Coupling(name='Constraint-Load'+str(order), controlPoint=region1, 
        #         surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC, 
        #         localCsys=None, u1=ON, u2=ON, ur3=ON)

        #         a = mdb.models[MyModel._modelName].rootAssembly
        #         r1 = a.referencePoints
        #         refPoints1=(r1[id], )
        #         region = a.Set(referencePoints=refPoints1, name='Set-Load'+str(order))
        #         mdb.models[MyModel._modelName].ConcentratedForce(name='Load-'+str(order), createStepName='Step-'+str(order), 
        #         region=region, cf2=load, distributionType=UNIFORM, field='', 
        #         localCsys=None)

        def _setReferPoint(self,instanceName,height):
                a = mdb.models[MyModel._modelName].rootAssembly
                e1 = a.instances[instanceName].edges
                r=a.ReferencePoint(point=a.instances[instanceName].InterestingPoint(edge=e1.findAt(
                coordinates=MyModel._sectionLength/2, height, 0)), rule=MIDDLE))
                a.Set(referencePoints=r, name='RefPoint-'+instanceName)
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

                self._createLoadingPlate()

                a = mdb.models[MyModel._modelName].rootAssembly
                region = a.sets['RefPoint-UpperPlate']

                self._createAMP()
                mdb.models['Model-Default'].DisplacementBC(name='Loading', 
                createStepName='Step-1', region=region, u1=0.0, u2=dsp, ur3=0.0, 
                amplitude='SmoothStepAMP', fixed=OFF, distributionType=UNIFORM, fieldName='', 
                localCsys=None)


                # a = mdb.models[MyModel._modelName].rootAssembly
                # r1 = a.referencePoints
                # refPoints1=(r1[id], )
                # region1=a.Set(referencePoints=refPoints1, name='m_Set-Load'+str(order))
                # a = mdb.models[MyModel._modelName].rootAssembly
                # s1 = a.instances[MyModel._concretePartName].edges
                # side1Edges1 = s1.findAt(((37.5, MyModel._sectionHeight, 0.0), ))
                # region2=a.Surface(side1Edges=side1Edges1, name='s_Surf-Load'+str(order))
                # mdb.models[MyModel._modelName].Coupling(name='Constraint-Load'+str(order), controlPoint=region1, 
                # surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC, 
                # localCsys=None, u1=ON, u2=ON, ur3=ON)

                # a = mdb.models[MyModel._modelName].rootAssembly
                # r1 = a.referencePoints
                # refPoints1=(r1[id], )
                # region = a.Set(referencePoints=refPoints1, name='Set-Load'+str(order))
                # mdb.models[MyModel._modelName].TabularAmplitude(name='Amp-1', timeSpan=STEP, smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (1.0, 1.0)))
                # mdb.models[MyModel._modelName].DisplacementBC(name='BC-Load-'+str(order), createStepName='Step-'+str(order), 
                # region=region, u1=UNSET, u2=dsp, ur3=UNSET, amplitude='Amp-1', fixed=OFF, 
                # distributionType=UNIFORM, fieldName='', localCsys=None)
                # try:
                #         mdb.models[MyModel._modelName].boundaryConditions['BC-Load-'+str(order)].deactivate('Step-'+str(order+1))
                # except:
                #         pass





                
