from AbaqusFiles import main_PartGen
from AbaqusFiles import main_Property
from AbaqusFiles import main_PartAssem
from AbaqusFiles import main_Interaction
from AbaqusFiles import main_Load
from AbaqusFiles import main_Mesh
from AbaqusFiles import main_Step
from AbaqusFiles import main_Job

class dspLoad():

    def setImportFile(self,CircleFileName='Circle.txt',InterFaceFileName='ringData.txt',innerCircleFileName='innerCircleData.txt'):
        import numpy as np
        self.circleData = np.loadtxt(CircleFileName)
        self.interfaceData=np.loadtxt(InterFaceFileName)#load the interface data
        self.innerCircleData=np.loadtxt(innerCircleFileName)
        self.CoarseAggregate=[]
        self.interface=[]
        self.partNumbers=len(self.circleData)
        for number in range(self.partNumbers):
            self.CoarseAggregate.append('CoarseAggregate-'+str(number))
            self.interface.append('interface-'+str(number))

    
    def setImportMaterial(self,GraniteElastic,InterfaceElastic):
        
    
    def __CreatePart():
