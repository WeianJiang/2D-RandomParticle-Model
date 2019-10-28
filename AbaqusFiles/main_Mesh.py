from abaqus import *
from abaqusConstants import *


def Mesh(modelName,partname,seedSize):
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


def createMeshPart(modelName):#---no use anymore, because the interation is too difficult
    p = mdb.models[modelName].parts['MainPart']
    p.PartFromMesh(name='MainPart-mesh-1', copySets=True)
    p1 = mdb.models['Model-1'].parts['MainPart-mesh-1']
    # del mdb.models[modelName].parts['MainPart']
    # mdb.models[modelName].parts.changeKey(fromName='MainPart-mesh-1', 
    # toName='MainPart')


def getEleNum(modelName):
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