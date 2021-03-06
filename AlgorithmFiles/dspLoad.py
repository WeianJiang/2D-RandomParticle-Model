from AbaqusFiles.main_initial import createModel
from AbaqusFiles.main_Part import PartModule
from AbaqusFiles.main_Property import PropertyModule
from AbaqusFiles.main_Assembly import AssemblyModule
from AbaqusFiles.main_Step import StepModule
from AbaqusFiles.main_Load import LoadModule
from AbaqusFiles.main_Mesh import MeshModule
from AbaqusFiles.main_Job import JobModule
from AbaqusFiles.Components.SteelBar import SteelBar_module

from AbaqusFiles.ModelModule import MyModel

import numpy as np
class dspLoad(MyModel):

    setReinforcement=False

    def _setImportFile(self,CircleFileName='Circle.txt'):
        self.circleData = np.loadtxt('ModelInfoFiles/'+str(MyModel._path)+'/'+CircleFileName)
        MyModel._circleNum=len(self.circleData)

    
    # def _setImportMaterial(self,GraniteElasticFileName='GraniteElastic.txt',InterfaceElasticFileName='interfaceElastic.txt'):
    #     self.GraniteElastic=np.loadtxt('ModelInfoFiles/'+str(MyModel._path)+'/'+GraniteElasticFileName)
    #     self.interfaceElastic=np.loadtxt('ModelInfoFiles/'+str(MyModel._path)+'/'+InterfaceElasticFileName)
    
    def setPath(self,path=1,name='Default'):
        MyModel._path=path
        MyModel._modelName='Model-'+str(name)
        self._setImportFile()
        # self._setImportMaterial()
        createModel()

    def setSize(self,length,height):
        MyModel._sectionLength=length
        MyModel._sectionHeight=height


    def _Part(self):#create partition of circles
        myPart=PartModule()
        myPart.createPart(self.circleData)
    
    def _Material(self):

        Aggregate=PropertyModule('Aggregate')
        Aggregate.materialCreate(51246,0.3,2.7e-9)

        Interface=PropertyModule('Interface')
        Interface.materialCreate(2.56E+04,0.2,2e-9)

        Matrix=PropertyModule('Matrix')
        Matrix.materialCreate(3.29E+04,0.2,2e-9)

    
    def _Assembly(self):
        myAssembly=AssemblyModule()
        myAssembly.partInst()

        if self.setReinforcement:
            steelbars=SteelBar_module(10)
            steelbars.setEnlargementofStirrup(225,450)
            steelbars.setNumberofLongui(2)
            steelbars.setSpacingofStir(32.14,75)
            steelbars.setStirrupMate(6,235)
            steelbars.setLonguiBarMate(10,335)

        # if self.setReinforcement:
        #     steelbars=SteelBar_module(10)
        #     steelbars.setEnlargementofStirrup(225,450)
        #     steelbars.setNumberofLongui(6)
        #     steelbars.setSpacingofStir(32.14,75)
        #     steelbars.setStirrupMate(6,235)
        #     steelbars.setLonguiBarMate(10,335)


    
    def _Interaction(self):
        pass
        # for number in range(self.partNumbers):
        #     main_Interaction.creatingTie(self.Model,self.interface[number],self.CoarseAggregate[number],self.innerCircleData[number][0],
        #         self.innerCircleData[number][1],self.innerCircleData[number][2],number)
        #     main_Interaction.creatingTie(self.Model,'MainPart',self.interface[number],self.interfaceData[number][0],
        #         self.interfaceData[number][1],self.interfaceData[number][2],number)

    
    def _Step(self):

        Step1=StepModule()
        Step1.createStep()
        # self.stepNum=1
        # if self.stepNum>1:
        #     for i in range(self.stepNum):
        #         if i+2<=self.stepNum:
        #             main_Step.createStep('Step-'+str(i+2),'Step-'+str(i+1))


    def _Load(self):

        load1=LoadModule()
        load1.setReferDspLoad(self.loadDsp)

    def setLoadDsp(self,loadDsp):
        self.loadDsp=loadDsp
        self._Job()

    def _Mesh(self):#apply mesh control here
        MeshPart=MeshModule(self.circleData)
        MeshPart.SeedMatrix(4)
        MeshPart.SeedByEdge(3,2,5)
        MeshPart.MeshType('Particle','TRI','FREE')
        MeshPart.MeshType('Interface','TRI','FREE')
        MeshPart.MeshType('Matrix','QUAD','FREE')
        MeshPart.SeedLoadingPlate(20)
        # MeshPart.MeshType('Interface','QUAD','SWEEP')
        # MeshPart.MeshType('Matrix','QUAD_DOMINATED','FREE')


        # for number in range(self.partNumbers):
        #     main_Mesh.Mesh(self.Model,self.CoarseAggregate[number],2)
        #     #main_Mesh.Mesh(interface[number],interfaceData[number][3]/10/2)
        #     main_Mesh.Mesh(self.Model,self.interface[number],2)

    # def _MeshfromPart(self):
        # main_Mesh.createMeshPart(self.Model)
        # self.MeshPartEleNum=main_Mesh.getEleNum(self.Model)
        # print self.MeshPartEleNum

    def _Job(self):
        self._Part()
        self._Material()
        self._Assembly()
        self._Interaction()
        self._Step()
        self._Load()
        self._Mesh()
        job1=JobModule()
        job1.createJob('Job-'+str(MyModel._modelName))
        
        

    



