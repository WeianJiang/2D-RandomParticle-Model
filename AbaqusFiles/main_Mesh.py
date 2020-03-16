from abaqus import *
from abaqusConstants import *

class Mesh():

    def __init__(self,modelName,partname,circleData=[]):
        self.__modelName=modelName
        self.__partname=partname
        self.__circleData=circleData
        self.__partNumbers=len(circleData)


    def SeedInterfaceByEdge(self,seedSize):
        p = mdb.models[self.__modelName].parts[self.__partname]
        e = p.edges
        for i in range(self.__partNumbers):
            target_x=self.__circleData[i][0]
            target_y=self.__circleData[i][1]
            radi=self.__circleData[i][2]
            #the inner circle seed
            pickedEdges = e.findAt(((target_x+0.9*radi, target_y, 0.0), ))
            p.seedEdgeBySize(edges=pickedEdges, size=seedSize, deviationFactor=0.1, 
                constraint=FINER)
            #the outter circle seed
            pickedEdges = e.findAt(((target_x+radi, target_y, 0.0), ))
            p.seedEdgeBySize(edges=pickedEdges, size=seedSize, deviationFactor=0.1, 
                constraint=FINER)

    def SeedMatrix(self,seedsize):
        p = mdb.models[self.__modelName].parts[self.__partname]
        p.seedPart(size=seedsize, deviationFactor=0.1, minSizeFactor=0.1)


    def MeshType(self,part,meshtype='TRI',technq='FREE'):
        '''
        part=Particle,Interface,Matrix
        meshtype=TRI,QUAD,QUAD_DOMINATED
        technq=FREE,SWEEP
        '''
        p = mdb.models[self.__modelName].parts[self.__partname]
        f = p.faces
        if meshtype=='TRI':
            meshtype=TRI
        elif meshtype=='QUAD':
            meshtype=QUAD
        elif meshtype=='QUAD_DOMINATED':
            meshtype=QUAD_DOMINATED
        if technq=='FREE':
            technq=FREE 
        elif technq=='SWEEP':
            technq=SWEEP
        if part=='Particle':
            for i in range(self.__partNumbers):
                target_x=self.__circleData[i][0]
                target_y=self.__circleData[i][1]
                pickedRegions = f.findAt(((target_x, target_y, 0.0), ))
                p.setMeshControls(regions=pickedRegions, elemShape=meshtype,technique=technq)
        elif part=='Interface':
            for i in range(self.__partNumbers):
                target_x=self.__circleData[i][0]
                target_y=self.__circleData[i][1]
                radi=self.__circleData[i][2]
                pickedRegions = f.findAt(((target_x+0.95*radi, target_y, 0.0), ))
                p.setMeshControls(regions=pickedRegions, elemShape=meshtype, technique=technq)
        elif part=='Matrix':
            pickedRegions = f.findAt(((0, 0, 0.0), ))
            p.setMeshControls(regions=pickedRegions, elemShape=meshtype, technique=technq)


    def Mesh(self,modelName,partname,seedSize):
        p = mdb.models[modelName].parts[partname]
        f = p.faces
        pickedRegions = f.getSequenceFromMask(mask=('[#1 ]', ), )
        p.setMeshControls(regions=pickedRegions, elemShape=TRI)
        #----------Seeding
        p = mdb.models[modelName].parts[partname]
        p.seedPart(size=seedSize, deviationFactor=0.1, minSizeFactor=0.1)
        #---------------mesh
        p = mdb.models[modelName].parts[partname]
        p.generateMesh()


    def createMeshPart(self,modelName):#---no use anymore, because the interation is too difficult
        p = mdb.models[modelName].parts['MainPart']
        p.PartFromMesh(name='MainPart-mesh-1', copySets=True)
        p1 = mdb.models['Model-1'].parts['MainPart-mesh-1']
        # del mdb.models[modelName].parts['MainPart']
        # mdb.models[modelName].parts.changeKey(fromName='MainPart-mesh-1', 
        # toName='MainPart')


    def getEleNum(self,modelName):
        p = mdb.models[modelName].parts['MainPart']
        e = p.elements
        return len(e)


    def createSetforEle(modelName):
        p = mdb.models[modelName].parts['MainPart']
        e = p.elements
        totalNum=getEleNum(modelName)
        for i in range(totalNum):
            elements = e[i:i+1]
            p.Set(elements=elements, name='Set-Mesh-'+str(i))

    def assignSectionToSet(modelName,section,meshSet):
        #mesh set in naming rule "Set-Mesh-i"
        p = mdb.models[modelName].parts['MainPart']
        region = p.sets[meshSet]
        p = mdb.models[modelName].parts['MainPart']
        p.SectionAssignment(region=region, sectionName=section, offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', 
            thicknessAssignment=FROM_SECTION)

if __name__=='__main__':
    pass