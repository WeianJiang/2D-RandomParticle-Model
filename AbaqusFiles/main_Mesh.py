from abaqus import *
from abaqusConstants import *

from ModelModule import MyModel

class MeshModule(MyModel):

    def __init__(self,circleData=[]):
        self.__circleData=circleData
        


    def SeedByEdge(self,seedSize):
        p = mdb.models[MyModel._modelName].parts[MyModel._concretePartName]
        e = p.edges
        for i in range(MyModel._circleNum):

            #getting basic information
            target_x=self.__circleData[i][0]
            target_y=self.__circleData[i][1]
            radi=self.__circleData[i][2]

            #the Matrix/Tran edge
            pickedEdges = e.findAt(((target_x+radi, target_y, 0.0), ))
            p.seedEdgeBySize(edges=pickedEdges, size=seedSize, deviationFactor=0.1, 
                constraint=FINER)

            #the Tran/Interface edge
            pickedEdges = e.findAt(((target_x+0.9*radi, target_y, 0.0), ))
            p.seedEdgeBySize(edges=pickedEdges, size=seedSize, deviationFactor=0.1, 
                constraint=FINER)
            
            #the Interface/Aggregate edge
            pickedEdges = e.findAt(((target_x+0.8*radi, target_y, 0.0), ))
            p.seedEdgeBySize(edges=pickedEdges, size=seedSize, deviationFactor=0.1, 
                constraint=FINER)


            #the Aggregate/Interface edge
            pickedEdges = e.findAt(((target_x+0.7*radi, target_y, 0.0), ))
            p.seedEdgeBySize(edges=pickedEdges, size=seedSize, deviationFactor=0.1, 
                constraint=FINER)

    def SeedMatrix(self,seedsize):
        p = mdb.models[MyModel._modelName].parts[MyModel._concretePartName]
        p.seedPart(size=seedsize, deviationFactor=0.1, minSizeFactor=0.1)


    def MeshType(self,part,meshtype='TRI',technq='FREE'):
        '''
        part=Particle,Interface,Matrix
        meshtype=TRI,QUAD,QUAD_DOMINATED
        technq=FREE,SWEEP
        '''
        p = mdb.models[MyModel._modelName].parts[MyModel._concretePartName]
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
            for i in range(MyModel._circleNum):
                target_x=self.__circleData[i][0]
                target_y=self.__circleData[i][1]
                pickedRegions = f.findAt(((target_x, target_y, 0.0), ))
                p.setMeshControls(regions=pickedRegions, elemShape=meshtype,technique=technq)
        elif part=='Interface':
            for i in range(MyModel._circleNum):
                target_x=self.__circleData[i][0]
                target_y=self.__circleData[i][1]
                radi=self.__circleData[i][2]
                pickedRegions = f.findAt(((target_x+0.95*radi, target_y, 0.0), ))
                p.setMeshControls(regions=pickedRegions, elemShape=meshtype, technique=technq)
        elif part=='Matrix':
            pickedRegions = f.findAt(((0, 0, 0.0), ))
            p.setMeshControls(regions=pickedRegions, elemShape=meshtype, technique=technq)


    def Mesh(self,seedSize):
        p = mdb.models[MyModel._modelName].parts[MyModel._concretePartName]
        f = p.faces
        pickedRegions = f.getSequenceFromMask(mask=('[#1 ]', ), )
        p.setMeshControls(regions=pickedRegions, elemShape=TRI)
        #----------Seeding
        p = mdb.models[MyModel._modelName].parts[MyModel._concretePartName]
        p.seedPart(size=seedSize, deviationFactor=0.1, minSizeFactor=0.1)
        #---------------mesh
        p = mdb.models[MyModel._modelName].parts[MyModel._concretePartName]
        p.generateMesh()


    # def createMeshPart(self):#---no use anymore, because the interation is too difficult
    #     p = mdb.models[MyModel._modelName].parts['MainPart']
    #     p.PartFromMesh(name='MainPart-mesh-1', copySets=True)
    #     p1 = mdb.models['Model-1'].parts['MainPart-mesh-1']
    #     # del mdb.models[modelName].parts['MainPart']
    #     # mdb.models[modelName].parts.changeKey(fromName='MainPart-mesh-1', 
    #     # toName='MainPart')


    def getEleNum(self):
        p = mdb.models[MyModel._modelName].parts['MainPart']
        e = p.elements
        return len(e)


    def createSetforEle(self):
        p = mdb.models[MyModel._modelName].parts['MainPart']
        e = p.elements
        totalNum=getEleNum(MyModel._modelName)
        for i in range(totalNum):
            elements = e[i:i+1]
            p.Set(elements=elements, name='Set-Mesh-'+str(i))

    def assignSectionToSet(self,section,meshSet):
        #mesh set in naming rule "Set-Mesh-i"
        p = mdb.models[MyModel._modelName].parts['MainPart']
        region = p.sets[meshSet]
        p = mdb.models[MyModel._modelName].parts['MainPart']
        p.SectionAssignment(region=region, sectionName=section, offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', 
            thicknessAssignment=FROM_SECTION)

if __name__=='__main__':
    pass