from abaqus import *
from abaqusConstants import *


def materialCreate(materialName,elaticModules,possionRatio,density):
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

def DPassign(materialName):
        mdb.models['Model-1'].materials[materialName].DruckerPrager(table=((64.0, 0.0, 64.0), ))
        mdb.models['Model-1'].materials[materialName].druckerPrager.DruckerPragerHardening(
    table=((29.0, 0.0), (30.0, 0.002), (20.0, 0.003), (10.0, 0.004), (5.0, 
    0.006)))