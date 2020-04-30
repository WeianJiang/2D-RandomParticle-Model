from abaqus import *
from abaqusConstants import *

from ModelModule import MyModel

class PartModule(MyModel):

    def _partRectGen(self):
        s = mdb.models[MyModel._modelName].ConstrainedSketch(name='__profile__', 
        sheetSize=200)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)
        s.rectangle(point1=(0.0, 0.0), point2=(MyModel._sectionLength, MyModel._sectionHeight))
        p = mdb.models[MyModel._modelName].Part(name=MyModel._concretePartName, dimensionality=TWO_D_PLANAR, 
            type=DEFORMABLE_BODY)
        p = mdb.models[MyModel._modelName].parts[MyModel._concretePartName]
        p.BaseShell(sketch=s)
        s.unsetPrimaryObject()
        p = mdb.models[MyModel._modelName].parts[MyModel._concretePartName]
        del mdb.models[MyModel._modelName].sketches['__profile__']
    


    def _partCircleGen(self,circleData=[]):
        p = mdb.models[MyModel._modelName].parts[MyModel._concretePartName]
        f, e, d1 = p.faces, p.edges, p.datums
        t = p.MakeSketchTransform(sketchPlane=f.findAt(coordinates=(50.0, 50.0, 0.0), 
            normal=(0.0, 0.0, 1.0)), sketchPlaneSide=SIDE1, origin=(0, 0, 0.0))
        s1 = mdb.models[MyModel._modelName].ConstrainedSketch(name='__profile__', 
            sheetSize=424.26, gridSpacing=10.6, transform=t)
        g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
        s1.setPrimaryObject(option=SUPERIMPOSE)
        p = mdb.models[MyModel._modelName].parts[MyModel._concretePartName]
        p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
        particleNumbers=len(circleData)
        for number in range(particleNumbers):
            target_x=circleData[number][0]
            target_y=circleData[number][1]
            radi=circleData[number][2]
            #the circle is regarded as the outter boundary of transition zone,
            s1.CircleByCenterPerimeter(center=(target_x, target_y), point1=(target_x+0.7*radi, target_y))#the aggregate /transition zone,
            s1.CircleByCenterPerimeter(center=(target_x, target_y), point1=(target_x+0.8*radi, target_y))#the aggregate /transition zone,let it be 1/10 of the radi
            s1.CircleByCenterPerimeter(center=(target_x, target_y), point1=(target_x+0.9*radi, target_y))#the interface, 1/10 of the radi
            s1.CircleByCenterPerimeter(center=(target_x, target_y), point1=(target_x+radi, target_y))#the outter-most circle, the transition zone
            #0.9~1, the transition zone, the matrix property
            #0.8~0.9, the interface zone, the interface property
            #0.7~0.8, the transition zone, the aggregate property
            #~0.7, the aggrefate property
            
        p = mdb.models[MyModel._modelName].parts[MyModel._concretePartName]
        f = p.faces
        pickedFaces = f.findAt(((50.0, 50.0, 0.0), ))
        e1, d2 = p.edges, p.datums
        p.PartitionFaceBySketch(faces=pickedFaces, sketch=s1)
        s1.unsetPrimaryObject()
        del mdb.models[MyModel._modelName].sketches['__profile__']
        #procedure of create particle set
        for i in range(particleNumbers):
            target_x=circleData[i][0]
            target_y=circleData[i][1]
            radi=circleData[i][2]
            self._createSet(target_x,target_y,'ParticleSet-'+str(i))
            self._createSet(target_x+0.95*radi,target_y,'InterfaceSet-'+str(i))
        self._createSet(0,0,'MainPartSet')


    def _createSet(self,target_x,target_y,setName):
        p = mdb.models[MyModel._modelName].parts[MyModel._concretePartName]
        f = p.faces
        if setName[0]=='P':
            faces = f.findAt(((target_x, target_y, 0.0), (target_x+0.75*radi,target_y,0.0),))
            p.Set(faces=faces, name=setName)
        elif setName[0]=='I':
            faces = f.findAt(((target_x, target_y, 0.0), ))
            p.Set(faces=faces, name=setName)
        elif setName[0]=='M':
            





