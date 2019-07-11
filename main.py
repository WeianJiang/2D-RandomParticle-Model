from AbaqusFiles import main_PartGen
from AbaqusFiles import main_Property
from AbaqusFiles import main_PartAssem
from AbaqusFiles import main_Interaction
from AbaqusFiles import main_Load
from AbaqusFiles import main_Mesh
import numpy as np





circleData = np.loadtxt('Circle.txt')
partName=[]
for number in range(len(circleData)):
    partName.append('Part-'+str(number))

main_PartGen.partRectGen('MainPart',circleData)
GraniteElastic=np.loadtxt('GraniteElastic.txt')


for number in range(len(partName)):
    main_PartGen.partCircleGen(partName[number],circleData[number][0],circleData[number][1],circleData[number][2])
    main_Property.materialCreate(partName[number],GraniteElastic[number],0.3)#property of rock
    main_Property.sectionCreate(partName[number],partName[number])
    main_Property.assignSection(partName[number],partName[number])

main_Property.materialCreate('MainPart',134000,0.3)#property of mortar
main_Property.sectionCreate('MainPart','MainPart')
main_Property.assignSection('MainPart','MainPart')

main_PartAssem.partInst('MainPart')
map(main_PartAssem.partInst,partName)

for number in range(len(partName)):
    main_Interaction.creatingTie('MainPart',partName[number],circleData[number][0],circleData[number][1],circleData[number][2],number)


#-----------------------------step
mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')

main_Load.setLoad('MainPart',1000,1)
main_Load.setBoundary('MainPart',1)

main_Mesh.Mesh('MainPart',14)
map(main_Mesh.Mesh,partName,14)
