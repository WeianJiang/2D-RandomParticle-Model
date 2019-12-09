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
from randomGenerator import weibullGenrator

class MeshPartModel(dspLoad):

    def __init__(self):
        print 'Using MeshfromPart'
    
    def _Material(self):
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
        
    
    def _MeshfromPart(self):
        main_Mesh.createSetforEle(self.Model)
        MeshEleNum=main_Mesh.getEleNum(self.Model)
        for i in range(MeshEleNum):
            main_Property.materialCreate(self.Model,'Mesh-Mate-'+str(i),weibullGenrator(1.5,23000),0.2,2e-09)# generating properties for each element set
            main_Property.sectionCreate(self.Model,'Mesh-'+str(i),'Mesh-Mate-'+str(i))
            main_Mesh.assignSectionToSet(self.Model,'Mesh-'+str(i),'Set-Mesh-'+str(i))


    def _Interaction(self):
        for number in range(self.partNumbers):
            main_Interaction.creatingTie(self.Model,self.interface[number],self.CoarseAggregate[number],self.innerCircleData[number][0],
                self.innerCircleData[number][1],self.innerCircleData[number][2],number)
            main_Interaction.creatingTie(self.Model,'MainPart',self.interface[number],self.interfaceData[number][0],
                self.interfaceData[number][1],self.interfaceData[number][2],number)

    def _Load(self):
        main_Load.setBoundary(self.Model,'MainPart',1)#set the boundary
        index=main_Load.setReferPoint(self.Model)
        dsp=self.loadDsp
        # for i in range(self.stepNum):
        # #     main_Load.setLoad('MainPart',6000/stepNum,i+1)
        #     # main_Load.setReferConLoad(-6500/stepNum,i+1,index)
        #     dsp=-0.2/self.stepNum+dsp
        #     #main_Load.setDspLoad('MainPart',dsp,i+1)
        main_Load.setReferDspLoad(self.Model,'MainPart',dsp,1,index)

    def _Job(self):
        self._Material()
        self._Assembly()
        self._Mesh()
        self._MeshfromPart()
        self._Assembly()
        self._Interaction()
        self._Step()
        self._Load()
        main_Job.createJob(self.Model,self.jobName,6)
