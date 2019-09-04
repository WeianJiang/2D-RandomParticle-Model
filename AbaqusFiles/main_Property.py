from abaqus import *
from abaqusConstants import *


def materialCreate(materialName,elaticModules,possionRatio):
    mdb.models['Model-1'].Material(name=materialName)
    mdb.models['Model-1'].materials[materialName].Elastic(table=((float(elaticModules), float(possionRatio)), ))
    mdb.models['Model-1'].materials[materialName].Density(table=((density, ), ))


def sectionCreate(sectionName,materialName):
    mdb.models['Model-1'].HomogeneousSolidSection(name=sectionName, material=materialName, thickness=None)


def assignSection(partName,sectionName):
    p = mdb.models['Model-1'].parts[partName]
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region = p.Set(faces=faces, name='Set-1')
    p = mdb.models['Model-1'].parts[partName]
    p.SectionAssignment(region=region, sectionName=sectionName, offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)

def PLassign(materialName):
        import numpy as np
        Compress=np.loadtxt('Compression.txt')
        Tensile=np.loadtxt('Tension.txt')
        mdb.models['Model-1'].materials[materialName].ConcreteDamagedPlasticity(table=((
        38.0, 0.1, 1.16, 0.667, 0.0), ))
        mdb.models['Model-1'].materials[materialName].concreteDamagedPlasticity.ConcreteCompressionHardening(
        table=(Compress))
        mdb.models['Model-1'].materials[materialName].concreteDamagedPlasticity.ConcreteTensionStiffening(
        table=(Tensile))