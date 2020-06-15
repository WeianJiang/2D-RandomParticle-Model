from abaqus import *
from abaqusConstants import *

from AbaqusFiles.ModelModule import MyModel

class SteelBar_module(MyModel):

    def __init__(self,coverThickness,enlargement,nonEnlargement):
        self.coverThickness=coverThickness

    
    def setNumberofLongui(self,numberofLongui):
        self.numberofLongui=numberofLongui
    
    def setSpacingofStir(self,enlargementSpacingofStir,nonEnlargementSpacingofStir):
        self.enlargementSpacingofStir=enlargementSpacingofStir
        self.nonEnlargementSpacingofStir=nonEnlargementSpacingofStir
    
    def setEnlargementofStirrup(self,enlargement,nonEnlargement):
        self.enlargement=enlargement
        self.nonEnlargement=nonEnlargement

    def longiBarGeneration(self):
        pass

    def _stirrupGeneration(self):
        s = mdb.models[MyModel._modelName].ConstrainedSketch(name='__profile__', 
            sheetSize=200.0)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)
        s.Line(point1=(0.0, 0.0), point2=(MyModel._sectionLength-2*self.coverThickness, 0.0))
        s.HorizontalConstraint(entity=g[2], addUndoState=False)
        p = mdb.models[MyModel._modelName].Part(name='stirrup', dimensionality=TWO_D_PLANAR, 
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
        spacingofLongui=(MyModel._sectionLength-2*self.coverThickness)/self.numberofLongui
        spacing=self.coverThickness
        for i in range(self.numberofLongui):
            a.Instance(name='longuiBar-'+str(i), part=p, dependent=ON)
            a.translate(instanceList=('longuiBar-'+str(i), ), vector=(spacing,0.0, 0.0))
            spacing+=spacingofLongui

        #now assembly the stirrup
        p = mdb.models[MyModel._modelName].parts['stirrup']
        numberofEnlargeStirrup=self.enlargement/self.enlargementSpacingofStir
        numberofNonenlargeStirrup=self.nonEnlargement/self.nonEnlargementSpacingofStir
        stirHeight=self.coverThickness
        for i in range(numberofEnlargeStirrup):
            a.Instance(name='stirrup-'+str(i), part=p, dependent=ON)
            a.translate(instanceList=('longuiBar-'+str(i), ), vector=(self.coverThickness,stirHeight, 0.0))
            stirHeight+=self.enlargementSpacingofStir
        
        for j in range(numberofNonenlargeStirrup):
            a.Instance(name='stirrup-'+str(i+j+1), part=p, dependent=ON)
            a.translate(instanceList=('longuiBar-'+str(i+j+1), ), vector=(self.coverThickness,stirHeight, 0.0))
            stirHeight+=self.nonEnlargementSpacingofStir
        
        for k in range(numberofEnlargeStirrup):
            a.Instance(name='stirrup-'+str(i+j+k+1), part=p, dependent=ON)
            a.translate(instanceList=('longuiBar-'+str(i+j+k+1), ), vector=(self.coverThickness,stirHeight, 0.0))
            stirHeight+=self.enlargementSpacingofStir
