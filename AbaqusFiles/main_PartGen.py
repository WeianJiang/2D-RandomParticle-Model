from abaqus import *
from abaqusConstants import *


def partRectGen(partname, circleData=[]):
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=150.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.rectangle(point1=(0, 0), point2=(150, 150))#setCubic
    for number in range(len(circleData)):
        s.CircleByCenterPerimeter(center=(circleData[number][0], circleData[number][1]), point1=(circleData[number][0]+circleData[number][2],circleData[number][1])) #setCircle
    p = mdb.models['Model-1'].Part(name=partname, dimensionality=TWO_D_PLANAR, 
    type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts[partname]
    p.BaseShell(sketch=s)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts[partname]
    del mdb.models['Model-1'].sketches['__profile__']

def partCircleGen(partname,target_x,target_y,radi):#single CIrcle
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=150.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    s1.CircleByCenterPerimeter(center=(target_x,target_y), point1=(target_x+radi, target_y))#setCircle
    p = mdb.models['Model-1'].Part(name=partname, dimensionality=TWO_D_PLANAR, 
    type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts[partname]
    p.BaseShell(sketch=s1)
    s1.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts[partname]
    del mdb.models['Model-1'].sketches['__profile__']


def interfaceGen(partname,target_x,target_y,outterRadi,innerRadi):
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=150.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    s1.CircleByCenterPerimeter(center=(target_x,target_y), point1=(target_x+outterRadi, target_y))#set outter Circle
    s1.CircleByCenterPerimeter(center=(target_x,target_y), point1=(target_x+innerRadi, target_y))#set inner Circle
    p = mdb.models['Model-1'].Part(name=partname, dimensionality=TWO_D_PLANAR, 
    type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts[partname]
    p.BaseShell(sketch=s1)
    s1.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts[partname]
    del mdb.models['Model-1'].sketches['__profile__']


def createSplitPlate():
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=20.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.Line(point1=(70, 0.0), point2=(80, 0.0))
    s.HorizontalConstraint(entity=g[2], addUndoState=False)
    s.Line(point1=(80, 0.0), point2=(80, -1))
    s.VerticalConstraint(entity=g[3], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[2], entity2=g[3], addUndoState=False)
    s.Line(point1=(80, -1), point2=(70, -1))
    s.HorizontalConstraint(entity=g[4], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
    s.Line(point1=(70, -1), point2=(70, 0.0))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)
    p = mdb.models['Model-1'].Part(name='LowerPlate', dimensionality=TWO_D_PLANAR, 
        type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['LowerPlate']
    p.BaseShell(sketch=s)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['LowerPlate']
    del mdb.models['Model-1'].sketches['__profile__']

    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=20.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    s1.Line(point1=(70, 150.0), point2=(80, 150.0))
    s1.HorizontalConstraint(entity=g[2], addUndoState=False)
    s1.Line(point1=(80, 150.0), point2=(80, 151))
    s1.VerticalConstraint(entity=g[3], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[2], entity2=g[3], addUndoState=False)
    s1.Line(point1=(80, 151), point2=(70, 151))
    s1.HorizontalConstraint(entity=g[4], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
    s1.Line(point1=(70, 151), point2=(70,150))
    s1.VerticalConstraint(entity=g[5], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)
    p = mdb.models['Model-1'].Part(name='UpperPlate', dimensionality=TWO_D_PLANAR, 
    type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['UpperPlate']
    p.BaseShell(sketch=s1)
    s1.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['UpperPlate']
    del mdb.models['Model-1'].sketches['__profile__']