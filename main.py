from AbaqusFiles import main_PartGen
from AbaqusFiles import main_Property
from AbaqusFiles import main_PartAssem
from AbaqusFiles import main_Interaction
from AbaqusFiles import main_Load
from AbaqusFiles import main_Mesh
import numpy as np





circleData = np.loadtxt('Circle.txt')
interfaceData=np.loadtxt('ringData.txt')#load the interface data
innerCircleData=np.loadtxt('innerCircleData.txt')
CoarseAggregate=[]
interface=[]
partNumbers=len(circleData)
for number in range(partNumbers):
    CoarseAggregate.append('CoarseAggregate-'+str(number))
    interface.append('interface-'+str(number))
#part generating----------------------------------------
main_PartGen.partRectGen('MainPart',circleData)#generating the retangle
GraniteElastic=np.loadtxt('GraniteElastic.txt')


for number in range(partNumbers):
    main_PartGen.partCircleGen(CoarseAggregate[number],circleData[number][0],circleData[number][1],circleData[number][2])
    main_Property.materialCreate(CoarseAggregate[number],GraniteElastic[number],0.3)#property of rock
    main_Property.sectionCreate(CoarseAggregate[number],CoarseAggregate[number])
    main_Property.assignSection(CoarseAggregate[number],CoarseAggregate[number])

main_Property.materialCreate('MainPart',134000,0.3)#property of mortar
main_Property.sectionCreate('MainPart','MainPart')
main_Property.assignSection('MainPart','MainPart')

main_PartAssem.partInst('MainPart')
map(main_PartAssem.partInst,CoarseAggregate)

for number in range(partNumbers):
    main_Interaction.creatingTie('MainPart',CoarseAggregate[number],circleData[number][0],circleData[number][1],circleData[number][2],number)


#-----------------------------step
mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')

main_Load.setLoad('MainPart',1000,1)
main_Load.setBoundary('MainPart',1)

main_Mesh.Mesh('MainPart',14)

for number in range(partNumbers):
    main_Mesh.Mesh(CoarseAggregate[number],2)
