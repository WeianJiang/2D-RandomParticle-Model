from AbaqusFiles import main_PartGen
from AbaqusFiles import main_Property
from AbaqusFiles import main_PartAssem
from AbaqusFiles import main_Interaction
from AbaqusFiles import main_Load
from AbaqusFiles import main_Mesh
from AbaqusFiles import main_Step
from AbaqusFiles import main_Job
import numpy as np
from dspLoad import dspLoad

class MeshPartModel(dspLoad):
    
    def __Material(self):
        for number in range(self.partNumbers):#here, all components are generated and material created, section assigned.
            main_PartGen.partCircleGen(self.Model,self.CoarseAggregate[number],self.innerCircleData[number][0],
                self.innerCircleData[number][1],self.innerCircleData[number][2])
            main_PartGen.interfaceGen(self.Model,self.interface[number],self.interfaceData[number][0],self.interfaceData[number][1],
                self.interfaceData[number][2],self.interfaceData[number][3])
            main_Property.materialCreate(self.Model,self.CoarseAggregate[number],self.GraniteElastic[number],0.3,2.7e-09)#property of rock
            main_Property.materialCreate(self.Model,self.interface[number],self.interfaceElastic[number],0.3,2e-09)
            main_Property.sectionCreate(self.Model,self.CoarseAggregate[number],self.CoarseAggregate[number])
            main_Property.sectionCreate(self.Model,self.interface[number],self.interface[number])
            main_Property.assignSection(self.Model,self.CoarseAggregate[number],self.CoarseAggregate[number])
            main_Property.assignSection(self.Model,self.interface[number],self.interface[number])

            main_PartGen.partRectGen(self.Model,'MainPart',self.circleData)#generating the retangle
    
    def __MeshfromPart(self):
        main_Mesh.createMeshPart(self.Model)
        self.MeshPartEleNum=main_Mesh.getEleNum(self.Model)
        print self.MeshPartEleNum


    def __Interaction(self):
        for number in range(self.partNumbers):
            main_Interaction.creatingTie(self.Model,self.interface[number],self.CoarseAggregate[number],self.innerCircleData[number][0],
                self.innerCircleData[number][1],self.innerCircleData[number][2],number)
            main_Interaction.creatingTie(self.Model,'MainPart',self.interface[number],self.interfaceData[number][0],
                self.interfaceData[number][1],self.interfaceData[number][2],number)

    def __Load(self):
        main_Load.setBoundary(self.Model,'MainPart',1)#set the boundary
        index=main_Load.setReferPoint(self.Model)
        dsp=self.loadDsp
        # for i in range(self.stepNum):
        # #     main_Load.setLoad('MainPart',6000/stepNum,i+1)
        #     # main_Load.setReferConLoad(-6500/stepNum,i+1,index)
        #     dsp=-0.2/self.stepNum+dsp
        #     #main_Load.setDspLoad('MainPart',dsp,i+1)
        main_Load.setReferDspLoad(self.Model,'MainPart',dsp,1,index)

    def __Job(self):
        self.__Material()
        self.__Mesh()
        self.__MeshfromPart()
        self.__Assembly()
        self.__Interaction()
        self.__Step()
        self.__Load()
        self.__Mesh()
        main_Job.createJob(self.Model,self.jobName,6)