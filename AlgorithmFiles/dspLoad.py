from AbaqusFiles import main_PartGen
from AbaqusFiles import main_Property
from AbaqusFiles import main_PartAssem
from AbaqusFiles import main_Interaction
from AbaqusFiles import main_Load
from AbaqusFiles import main_Mesh
from AbaqusFiles import main_Step
from AbaqusFiles import main_Job
import numpy as np
class dspLoad():

    def _setImportFile(self,CircleFileName='Circle.txt',InterFaceFileName='ringData.txt',innerCircleFileName='innerCircleData.txt'):
        self.circleData = np.loadtxt('ModelInfoFiles/'+str(self.path)+'/'+CircleFileName)
        self.CoarseAggregate=[]
        self.ParticleSet=[]
        self.interface=[]
        self.InterfaceSet=[]
        self.partNumbers=len(self.circleData)
        for number in range(self.partNumbers):
            self.CoarseAggregate.append('CoarseAggregate-'+str(number))
            self.interface.append('interface-'+str(number))
            self.InterfaceSet.append('InterfaceSet-'+str(number))
            self.ParticleSet.append('ParticleSet-'+str(number))

    
    def _setImportMaterial(self,GraniteElasticFileName='GraniteElastic.txt',InterfaceElasticFileName='interfaceElastic.txt'):
        self.GraniteElastic=np.loadtxt('ModelInfoFiles/'+str(self.path)+'/'+GraniteElasticFileName)
        self.interfaceElastic=np.loadtxt('ModelInfoFiles/'+str(self.path)+'/'+InterfaceElasticFileName)
    
    def setPath(self,path=1):
        self.Model='Model-'+str(path)
        self.path=path
        self._setImportFile()
        self._setImportMaterial()
        main_PartGen.createModel(self.Model)

    def setSize(self,Size=150):
        self.Size=Size

    def _Part(self):#create partition of circles
        main_PartGen.partRectGen(self.Model,'MainPart',self.Size)
        main_PartGen.partCircleGen(self.Model,'MainPart',self.circleData)
    
    def _Material(self):
        #first, create material:
        for number in range(self.partNumbers):
            main_Property.materialCreate(self.Model,self.CoarseAggregate[number],self.GraniteElastic[number],0.3,2.7e-09)
            main_Property.materialCreate(self.Model,self.interface[number],self.interfaceElastic[number],0.3,2e-09)
            main_Property.sectionCreate(self.Model,self.CoarseAggregate[number],self.CoarseAggregate[number])
            main_Property.sectionCreate(self.Model,self.interface[number],self.interface[number])
            main_Property.assignSection(self.Model,'MainPart',self.ParticleSet[number],self.CoarseAggregate[number])
            main_Property.assignSection(self.Model,'MainPart',self.InterfaceSet[number],self.interface[number])

        main_Property.materialCreate(self.Model,'MainPart',23000,0.2,2e-09)#property of mortar
        main_Property.PLMatCreate(self.Model,'MainPart',self.path)
    #     main_Property.interfacePLassign(self.Model,self.partNumbers,self.path)
        main_Property.sectionCreate(self.Model,'MainPart','MainPart')
        main_Property.assignSection(self.Model,'MainPart','MainPartSet','MainPart')

    
    def _Assembly(self):
        main_PartAssem.partInst(self.Model,'MainPart')


    
    def _Interaction(self):
        pass
        # for number in range(self.partNumbers):
        #     main_Interaction.creatingTie(self.Model,self.interface[number],self.CoarseAggregate[number],self.innerCircleData[number][0],
        #         self.innerCircleData[number][1],self.innerCircleData[number][2],number)
        #     main_Interaction.creatingTie(self.Model,'MainPart',self.interface[number],self.interfaceData[number][0],
        #         self.interfaceData[number][1],self.interfaceData[number][2],number)

    
    def _Step(self):

        main_Step.createStep(self.Model,'Step-1','Initial')
        # self.stepNum=1
        # if self.stepNum>1:
        #     for i in range(self.stepNum):
        #         if i+2<=self.stepNum:
        #             main_Step.createStep('Step-'+str(i+2),'Step-'+str(i+1))


    def _Load(self):
        main_Load.setBoundary(self.Model,'MainPart',self.Size,1)#set the boundary
        index=main_Load.setReferPoint(self.Model,self.Size)
        dsp=self.loadDsp
        # for i in range(self.stepNum):
        # #     main_Load.setLoad('MainPart',6000/stepNum,i+1)
        #     # main_Load.setReferConLoad(-6500/stepNum,i+1,index)
        #     dsp=-0.2/self.stepNum+dsp
        #     #main_Load.setDspLoad('MainPart',dsp,i+1)
        main_Load.setReferDspLoad(self.Model,'MainPart',dsp,self.Size,1,index)

    def setLoadDsp(self,loadDsp):
        self.loadDsp=loadDsp

    def _Mesh(self):
        MeshPart=main_Mesh.Mesh(self.Model,'MainPart',self.circleData)
        MeshPart.SeedMatrix(2)
        MeshPart.SeedInterfaceByEdge(0.1)
        MeshPart.MeshType('Particle','TRI','FREE')
        MeshPart.MeshType('Interface','QUAD','SWEEP')
        MeshPart.MeshType('Matrix','QUAD_DOMINATED','FREE')


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
        main_Job.createJob(self.Model,self.jobName,6)

    
    def setJobName(self,jobName):
        self.jobName=jobName
        self._Job()
    


