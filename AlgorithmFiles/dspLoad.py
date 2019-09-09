from AbaqusFiles import main_PartGen
from AbaqusFiles import main_Property
from AbaqusFiles import main_PartAssem
from AbaqusFiles import main_Interaction
from AbaqusFiles import main_Load
from AbaqusFiles import main_Mesh
from AbaqusFiles import main_Step
from AbaqusFiles import main_Job

class dspLoad():

    def __setImportFile(self,CircleFileName='Circle.txt',InterFaceFileName='ringData.txt',innerCircleFileName='innerCircleData.txt'):
        import numpy as np
        self.circleData = np.loadtxt(str(self.path)+CircleFileName)
        self.interfaceData=np.loadtxt(str(self.path)+InterFaceFileName)#load the interface data
        self.innerCircleData=np.loadtxt(str(self.path)+innerCircleFileName)
        self.CoarseAggregate=[]
        self.interface=[]
        self.partNumbers=len(self.circleData)
        for number in range(self.partNumbers):
            self.CoarseAggregate.append('CoarseAggregate-'+str(number))
            self.interface.append('interface-'+str(number))

    
    def __setImportMaterial(self,GraniteElasticFileName='GraniteElastic.txt',InterfaceElasticFileName='interfaceElastic.txt'):
        import numpy as np
        self.GraniteElastic=np.loadtxt(str(self.path)+GraniteElasticFileName)
        self.interfaceElastic=np.loadtxt(str(self.path)+InterfaceElasticFileName)
    
    def setPath(self,path='ModelInfoFiles/1/'):
        self.path=path
        self.__setImportFile(self)
        self.__setImportMaterial(self)

    
    def __Material(self):
        for number in range(self.partNumbers):#here, all components are generated and material created, section assigned.
            main_PartGen.partCircleGen(self.CoarseAggregate[number],self.innerCircleData[number][0],
                self.innerCircleData[number][1],self.innerCircleData[number][2])
            main_PartGen.interfaceGen(self.interface[number],self.interfaceData[number][0],self.interfaceData[number][1],
                self.interfaceData[number][2],self.interfaceData[number][3])
            main_Property.materialCreate(self.CoarseAggregate[number],self.GraniteElastic[number],0.3,2.7e-09)#property of rock
            main_Property.materialCreate(self.interface[number],self.interfaceElastic[number],0.3,2e-09)
            main_Property.sectionCreate(self.CoarseAggregate[number],self.CoarseAggregate[number])
            main_Property.sectionCreate(self.interface[number],self.interface[number])
            main_Property.assignSection(self.CoarseAggregate[number],self.CoarseAggregate[number])
            main_Property.assignSection(self.interface[number],self.interface[number])

            main_Property.materialCreate('MainPart',23000,0.2,2e-09)#property of mortar
            main_Property.PLassign('MainPart')
            main_Property.sectionCreate('MainPart','MainPart')
            main_Property.assignSection('MainPart','MainPart')

    
    def __Assembly(self):
        main_PartAssem.partInst('MainPart')
        map(main_PartAssem.partInst,self.CoarseAggregate)
        map(main_PartAssem.partInst,self.interface)

    
    def __Interaction(self):
        for number in range(self.partNumbers):
            main_Interaction.creatingTie(self.interface[number],self.CoarseAggregate[number],self.innerCircleData[number][0],
                self.innerCircleData[number][1],self.innerCircleData[number][2],number)
            main_Interaction.creatingTie('MainPart',self.interface[number],self.interfaceData[number][0],
                self.interfaceData[number][1],self.interfaceData[number][2],number)

    
    def __Step(self):

        main_Step.createStep('Step-1','Initial')
        # self.stepNum=1
        # if self.stepNum>1:
        #     for i in range(self.stepNum):
        #         if i+2<=self.stepNum:
        #             main_Step.createStep('Step-'+str(i+2),'Step-'+str(i+1))


    def __Load(self):
        main_Load.setBoundary('MainPart',1)#set the boundary
        index=main_Load.setReferPoint()
        dsp=self.loadDsp
        # for i in range(self.stepNum):
        # #     main_Load.setLoad('MainPart',6000/stepNum,i+1)
        #     # main_Load.setReferConLoad(-6500/stepNum,i+1,index)
        #     dsp=-0.2/self.stepNum+dsp
        #     #main_Load.setDspLoad('MainPart',dsp,i+1)
        main_Load.setReferDspLoad('MainPart',dsp,1,index)

    def setLoadDsp(self,loadDsp):
        self.loadDsp=loadDsp

    def __Mesh(self):
        main_Mesh.Mesh('MainPart',2)

        for number in range(self.partNumbers):
            main_Mesh.Mesh(self.CoarseAggregate[number],2)
            #main_Mesh.Mesh(interface[number],interfaceData[number][3]/10/2)
            main_Mesh.Mesh(self.interface[number],2)
    
    def __Job(self):
        self.__setImportFile()
        self.__setImportMaterial()
        self.__Material()
        self.__Assembly()
        self.__Interaction()
        self.__Step()
        self.__Load()
        self.__Mesh()
        main_Job.createJob(self.jobName)

    
    def setJobName(self,jobName):
        self.jobName=jobName