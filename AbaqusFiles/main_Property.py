from abaqus import *
from abaqusConstants import *


def materialCreate(modelName,materialName,elaticModules,possionRatio,density):
    mdb.models[modelName].Material(name=materialName)
    mdb.models[modelName].materials[materialName].Elastic(table=((float(elaticModules), float(possionRatio)), ))
    mdb.models[modelName].materials[materialName].Density(table=((density, ), ))



def sectionCreate(modelName,sectionName,materialName):
    mdb.models[modelName].HomogeneousSolidSection(name=sectionName, material=materialName, thickness=None)


def assignSection(modelName,partName,setName,sectionName):
    p = mdb.models[modelName].parts[partName]
    region = p.sets[setName]
    p = mdb.models[modelName].parts[partName]
    p.SectionAssignment(region=region, sectionName=sectionName, offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)


def PLMatCreate(modelName,materialName,ModelPathNumber):
    import numpy as np
    Compress=np.loadtxt('Constitution/'+str(ModelPathNumber)+'/Compression.txt')
    Tensile=np.loadtxt('Constitution/'+str(ModelPathNumber)+'/Tension.txt')
    TensionDamage=np.loadtxt('Constitution/'+str(ModelPathNumber)+'/TensionDamage.txt')
    CompressionDamage=np.loadtxt('Constitution/'+str(ModelPathNumber)+'/CompressionDamage.txt')
    mdb.models[modelName].materials[materialName].ConcreteDamagedPlasticity(table=((
    38.0, 0.1, 1.16, 0.667, 0.0), ))
    mdb.models[modelName].materials[materialName].concreteDamagedPlasticity.ConcreteCompressionHardening(
    table=(Compress))
    mdb.models[modelName].materials[materialName].concreteDamagedPlasticity.ConcreteTensionStiffening(
    table=(Tensile),type=STRAIN)
    mdb.models[modelName].materials['MainPart'].concreteDamagedPlasticity.ConcreteTensionDamage(
    table=TensionDamage, type=STRAIN) 
    mdb.models[modelName].materials['MainPart'].concreteDamagedPlasticity.ConcreteCompressionDamage(
    table=CompressionDamage) 


def interfacePLassign(modelName,interfaceNumbers,ModelPathNumber):
    import numpy as np
    Compress=np.loadtxt('Constitution/'+str(ModelPathNumber)+'/Compression.txt')
    Tensile=np.loadtxt('Constitution/'+str(ModelPathNumber)+'/Tension.txt')
    Compress=Compress/10
    Tensile=Tensile
    for i in range(interfaceNumbers):
        mdb.models[modelName].materials['interface-'+str(i)].ConcreteDamagedPlasticity(table=((
        38.0, 0.1, 1.16, 0.667, 0.0), ))
        mdb.models[modelName].materials['interface-'+str(i)].concreteDamagedPlasticity.ConcreteCompressionHardening(
        table=(Compress))
        mdb.models[modelName].materials['interface-'+str(i)].concreteDamagedPlasticity.ConcreteTensionStiffening(
        table=(Tensile),type=STRAIN)
        # mdb.models[modelName].materials[partName].concreteDamagedPlasticity.ConcreteTensionDamage(
        # table=TensionDamage, type=DISPLACEMENT) # NO need to use damage factor for monotonlic loading
        # mdb.models[modelName].materials['interface-'+str(i)].Damping(alpha=4.15, 
        # beta=4.83e-08)# NO need to input damping


def MeshMateCreate(modelName,materialName,elaticModules,possionRatio,density):
    mdb.models[modelName].Material(name=materialName)
    mdb.models[modelName].materials[materialName].Elastic(table=((float(elaticModules), float(possionRatio)), ))
    mdb.models[modelName].materials[materialName].Density(table=((density, ), ))
    
def PLMeshMaterialCreate(modelName,meshNumbers):
    import numpy as np
    Compress=[]
    Tension=[]
    ComDamage=[]
    TenDamage=[]
    Compress=np.loadtxt('ComMeshPl.txt')
    Tension=np.loadtxt('TenMeshPl.txt')
    ComDamage=np.loadtxt('ComDamage.txt')
    TenDamage=np.loadtxt('TenDamage.txt')
    # Compress=np.reshape(3,2)
    # Tension=np.reshape(3,2)
    # ComDamage=np.reshape(3,2)
    # TenDamage=np.reshape(3,2)
    for i in range(meshNumbers):
        materialName='Mesh-Mate-'+str(i)
        # mdb.models[modelName].Material(name=materialName)
        # mdb.models[modelName].materials[materialName].Elastic(table=((float(elaticModules), float(possionRatio)), ))
        # mdb.models[modelName].materials[materialName].Density(table=((density, ), ))
        mdb.models[modelName].materials[materialName].ConcreteDamagedPlasticity(table=((
        38.0, 0.1, 1.16, 0.667, 0.0), ))
        mdb.models[modelName].materials[materialName].concreteDamagedPlasticity.ConcreteCompressionHardening(
        table=(Compress[i].reshape(3,2)))
        mdb.models[modelName].materials[materialName].concreteDamagedPlasticity.ConcreteTensionStiffening(
        table=(Tension[i].reshape(3,2)),type=STRAIN)
        mdb.models[modelName].materials[materialName].concreteDamagedPlasticity.ConcreteTensionDamage(
        table=(TenDamage[i].reshape(3,2)), type=STRAIN)
        mdb.models[modelName].materials[materialName].Damping(alpha=4.15, 
        beta=4.83e-08)