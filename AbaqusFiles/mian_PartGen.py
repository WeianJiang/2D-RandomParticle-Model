from abaqus import *
from abaqusConstants import *


def partGen(partname):
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=150.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.rectangle(point1=(-75.0, 75.0), point2=(75.0, -75.0))
    s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(5.0, 0.0)) #setCircle
    p = mdb.models['Model-1'].Part(name=partname, dimensionality=TWO_D_PLANAR, 
    type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts[partname]
    p.BaseShell(sketch=s)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts[partname]