from abaqus import *
from abaqusConstants import *


def materialCreate(materialName,elaticModules,possionRatio):
    mdb.models['Model-1'].Material(name=materialName)
    mdb.models['Model-1'].materials[materialName].Elastic(table=((float(elaticModules), float(possionRatio)), ))


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
        mdb.models['Model-1'].materials[materialName].ConcreteDamagedPlasticity(table=((
        38.0, 0.1, 1.16, 0.667, 0.0), ))
        mdb.models['Model-1'].materials[materialName].concreteDamagedPlasticity.ConcreteCompressionHardening(
        table=((14.07, 0.0), (20.1, 0.000801898), (14.6366, 0.00245591), (10.0733, 
        0.00407992), (7.50085, 0.00563756), (5.93113, 0.00716179), (4.88986, 
        0.00866839), (4.15349, 0.0101648), (3.607, 0.011655), (3.18609, 
        0.0131409)))
        mdb.models['Model-1'].materials[materialName].concreteDamagedPlasticity.ConcreteTensionStiffening(
        table=((2.0301, 0.0), (2.01, 2.82563e-05), (1.23219, 0.00014944), (
        0.849073, 0.000257466), (0.660524, 0.000359008), (0.548371, 0.000458002), (
        0.473404, 0.000555757), (0.419357, 0.000652815), (0.378298, 0.00074944), (
        0.345892, 0.000845777), (0.118271, 0.00380631)))