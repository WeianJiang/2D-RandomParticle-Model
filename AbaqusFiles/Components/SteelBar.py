from abaqus import *
from abaqusConstants import *

from AbaqusFiles.ModelModule import MyModel

class SteelBar_module(MyModel):

    def __init__(self,coverThickness,enlargement,nonEnlargement):
        self.coverThickness=coverThickness
        self.enlargement=enlargement
        self.nonEnlargement=nonEnlargement
    
    def setNumberofLongui(self,numberofLongui):
        self.numberofLongui=numberofLongui
    
    def setSpacingofStir(self,spacingofStir):
        self.spacingofStir=spacingofStir

    def longiBarGeneration(self):
        pass

    def _stirrupGeneration(self):
        s = mdb.models[MyModel._modelName].ConstrainedSketch(name='__profile__', 
            sheetSize=200.0)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)
        s.Line(point1=(0.0, 0.0), point2=(MyModel._sectionLength-2*self.coverThickness, 0.0))
        s.HorizontalConstraint(entity=g[2], addUndoState=False)
        p = mdb.models[MyModel._modelName].Part(name='stir', dimensionality=TWO_D_PLANAR, 
            type=DEFORMABLE_BODY)
        # p = mdb.models['Model-1'].parts['Part-1']
        # p.BaseWire(sketch=s)
        # s.unsetPrimaryObject()
        del mdb.models['Model-1'].sketches['__profile__']

    def _longuiBarGeneration(self):
        s = mdb.models[MyModel._modelName].ConstrainedSketch(name='__profile__', 
            sheetSize=200.0)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)
        s.Line(point1=(0,0), point2=(0,MyModel._sectionHeight))
        s.HorizontalConstraint(entity=g[2], addUndoState=False)
        p = mdb.models[MyModel._modelName].Part(name='longuiBar', dimensionality=TWO_D_PLANAR, 
            type=DEFORMABLE_BODY)
        # p = mdb.models['Model-1'].parts['Part-1']
        # p.BaseWire(sketch=s)
        # s.unsetPrimaryObject()
        del mdb.models['Model-1'].sketches['__profile__']

    
    def _steelBarAssembly(self):
        a = mdb.models[MyModel._modelName].rootAssembly
        p = mdb.models[MyModel._modelName].parts['longuiBar']
        for i in range(self.numberofLongui):
            a.Instance(name='longuiBar-'+str(i), part=p, dependent=ON)
            a.translate(instanceList=('longuiBar-'+str(i), ), vector=(250.0,0.0, 0.0))