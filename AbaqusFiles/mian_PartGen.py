from abaqus import *
from abaqusConstants import *


def partRectGen(partname, circleData=[]):
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=150.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.rectangle(point1=(-75.0, 75.0), point2=(75.0, -75.0))#setCubic
    for number in range(len(circleData)):
        s.CircleByCenterPerimeter(center=(circleData[number][0], circleData[number][1]), point1=(circleData[number][0], circleData[number][2])) #setCircle
    p = mdb.models['Model-1'].Part(name=partname, dimensionality=TWO_D_PLANAR, 
    type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts[partname]
    p.BaseShell(sketch=s)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts[partname]


def partCircleGen(partname,circleData=[]):
    