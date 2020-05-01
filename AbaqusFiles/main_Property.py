from abaqus import *
from abaqusConstants import *

from ModelModule import MyModel

class PropertyModule(MyModel):

    def materialCreate(self,materialName,elaticModules,possionRatio,density):
        mdb.models[MyModel._modelName].Material(name=materialName)
        mdb.models[MyModel._modelName].materials[materialName].Elastic(table=((float(elaticModules), float(possionRatio)), ))
        mdb.models[MyModel._modelName].materials[materialName].Density(table=((density, ), ))



    def sectionCreate(self,sectionName,materialName):
        mdb.models[MyModel._modelName].HomogeneousSolidSection(name=sectionName, material=materialName, thickness=None)


    def assignSection(self,setName,sectionName):
        p = mdb.models[MyModel._modelName].parts[MyModel._concretePartName]
        region = p.sets[setName]
        p = mdb.models[MyModel._modelName].parts[MyModel._concretePartName]
        p.SectionAssignment(region=region, sectionName=sectionName, offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', 
            thicknessAssignment=FROM_SECTION)


    def PLMatCreate(self,materialName,ModelPathNumber):
        import numpy as np
        Compress=np.loadtxt('Constitution/'+str(ModelPathNumber)+'/Compression.txt')
        Tensile=np.loadtxt('Constitution/'+str(ModelPathNumber)+'/Tension.txt')
        TensionDamage=np.loadtxt('Constitution/'+str(ModelPathNumber)+'/TensionDamage.txt')
        CompressionDamage=np.loadtxt('Constitution/'+str(ModelPathNumber)+'/CompressionDamage.txt')
        mdb.models[MyModel._modelName].materials[materialName].ConcreteDamagedPlasticity(table=((
        38.0, 0.1, 1.16, 0.667, 0.0), ))
        mdb.models[MyModel._modelName].materials[materialName].concreteDamagedPlasticity.ConcreteCompressionHardening(
        table=(Compress))
        mdb.models[MyModel._modelName].materials[materialName].concreteDamagedPlasticity.ConcreteTensionStiffening(
        table=(Tensile),type=STRAIN)
        mdb.models[MyModel._modelName].materials['Matrix'].concreteDamagedPlasticity.ConcreteTensionDamage(
        table=TensionDamage, type=STRAIN) 
        mdb.models[MyModel._modelName].materials['Matrix'].concreteDamagedPlasticity.ConcreteCompressionDamage(
        table=CompressionDamage) 


    def interfacePLassign(self,interfaceNumbers,ModelPathNumber):
        import numpy as np
        Compress=np.loadtxt('Constitution/'+str(ModelPathNumber)+'/Compression.txt')
        Tensile=np.loadtxt('Constitution/'+str(ModelPathNumber)+'/Tension.txt')
        Compress=Compress/10
        Tensile=Tensile
        for i in range(interfaceNumbers):
            mdb.models[MyModel._modelName].materials['interface-'+str(i)].ConcreteDamagedPlasticity(table=((
            38.0, 0.1, 1.16, 0.667, 0.0), ))
            mdb.models[MyModel._modelName].materials['interface-'+str(i)].concreteDamagedPlasticity.ConcreteCompressionHardening(
            table=(Compress))
            mdb.models[MyModel._modelName].materials['interface-'+str(i)].concreteDamagedPlasticity.ConcreteTensionStiffening(
            table=(Tensile),type=STRAIN)
            # mdb.models[MyModel._modelName].materials[partName].concreteDamagedPlasticity.ConcreteTensionDamage(
            # table=TensionDamage, type=DISPLACEMENT) # NO need to use damage factor for monotonlic loading
            # mdb.models[MyModel._modelName].materials['interface-'+str(i)].Damping(alpha=4.15, 
            # beta=4.83e-08)# NO need to input damping


    def MeshMateCreate(self,materialName,elaticModules,possionRatio,density):
        mdb.models[MyModel._modelName].Material(name=materialName)
        mdb.models[MyModel._modelName].materials[materialName].Elastic(table=((float(elaticModules), float(possionRatio)), ))
        mdb.models[MyModel._modelName].materials[materialName].Density(table=((density, ), ))
        
    def PLMeshMaterialCreate(self,meshNumbers):
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
            # mdb.models[MyModel._modelName].Material(name=materialName)
            # mdb.models[MyModel._modelName].materials[materialName].Elastic(table=((float(elaticModules), float(possionRatio)), ))
            # mdb.models[MyModel._modelName].materials[materialName].Density(table=((density, ), ))
            mdb.models[MyModel._modelName].materials[materialName].ConcreteDamagedPlasticity(table=((
            38.0, 0.1, 1.16, 0.667, 0.0), ))
            mdb.models[MyModel._modelName].materials[materialName].concreteDamagedPlasticity.ConcreteCompressionHardening(
            table=(Compress[i].reshape(3,2)))
            mdb.models[MyModel._modelName].materials[materialName].concreteDamagedPlasticity.ConcreteTensionStiffening(
            table=(Tension[i].reshape(3,2)),type=STRAIN)
            mdb.models[MyModel._modelName].materials[materialName].concreteDamagedPlasticity.ConcreteTensionDamage(
            table=(TenDamage[i].reshape(3,2)), type=STRAIN)
            mdb.models[MyModel._modelName].materials[materialName].Damping(alpha=4.15, 
            beta=4.83e-08)