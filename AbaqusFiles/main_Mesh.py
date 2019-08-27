from abaqus import *
from abaqusConstants import *


def Mesh(partname,seedSize):
    p = mdb.models['Model-1'].parts[partname]
    f = p.faces
    pickedRegions = f.getSequenceFromMask(mask=('[#1 ]', ), )
    p.setMeshControls(regions=pickedRegions, elemShape=TRI)
    #----------Seeding
    p = mdb.models['Model-1'].parts[partname]
    p.seedPart(size=seedSize, deviationFactor=0.1, minSizeFactor=0.1)
    #---------------mesh
    p = mdb.models['Model-1'].parts[partname]
    p.generateMesh()