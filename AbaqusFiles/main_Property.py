from abaqus import *
from abaqusConstants import *


def materialCreate(modelName,materialName,elaticModules,possionRatio,density):
    mdb.models[modelName].Material(name=materialName)
    mdb.models[modelName].materials[materialName].Elastic(table=((float(elaticModules), float(possionRatio)), ))
    mdb.models[modelName].materials[materialName].Density(table=((density, ), ))


def sectionCreate(modelName,sectionName,materialName):
    mdb.models[modelName].HomogeneousSolidSection(name=sectionName, material=materialName, thickness=None)


def assignSection(modelName,partName,sectionName):
    p = mdb.models[modelName].parts[partName]
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region = p.Set(faces=faces, name='Set-1')
    p = mdb.models[modelName].parts[partName]
    p.SectionAssignment(region=region, sectionName=sectionName, offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)

def PLassign(modelName,materialName,ModelPathNumber):
        import numpy as np
        Compress=np.loadtxt('Constitution/'+str(ModelPathNumber)+'/Compression.txt')
        Tensile=np.loadtxt('Constitution/'+str(ModelPathNumber)+'/Tension.txt')
        TensionDamage=np.loadtxt('Constitution/'+str(ModelPathNumber)+'/TensionDamage.txt')
        mdb.models[modelName].materials[materialName].ConcreteDamagedPlasticity(table=((
        38.0, 0.1, 1.16, 0.667, 0.0), ))
        mdb.models[modelName].materials[materialName].concreteDamagedPlasticity.ConcreteCompressionHardening(
        table=(Compress))
        mdb.models[modelName].materials[materialName].concreteDamagedPlasticity.ConcreteTensionStiffening(
        table=(Tensile),type=DISPLACEMENT)
        mdb.models[modelName].materials['MainPart'].concreteDamagedPlasticity.ConcreteTensionDamage(
        table=TensionDamage, type=DISPLACEMENT)
        mdb.models[modelName].materials[materialName].Damping(alpha=4.15, 
        beta=4.83e-08)


def MeshMateCreate(modelName,materialName,elaticModules,possionRatio,density):
    mdb.models[modelName].Material(name=materialName)
    mdb.models[modelName].materials[materialName].Elastic(table=((float(elaticModules), float(possionRatio)), ))
    mdb.models[modelName].materials[materialName].Density(table=((density, ), ))
    