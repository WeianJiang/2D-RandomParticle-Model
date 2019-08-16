from AbaqusFiles import main_PartGen
from AbaqusFiles import main_Property
from AbaqusFiles import main_PartAssem
from AbaqusFiles import main_Interaction
from AbaqusFiles import main_Load
from AbaqusFiles import main_Mesh
from AbaqusFiles import main_Step
import numpy as np




#------------------------------------------------------------------------------------importing data
circleData = np.loadtxt('Circle.txt')
interfaceData=np.loadtxt('ringData.txt')#load the interface data
innerCircleData=np.loadtxt('innerCircleData.txt')
CoarseAggregate=[]
interface=[]
partNumbers=len(circleData)
for number in range(partNumbers):
    CoarseAggregate.append('CoarseAggregate-'+str(number))
    interface.append('interface-'+str(number))
#---------------------------------------------------------------------------------------part------------------------
main_PartGen.partRectGen('MainPart',circleData)#generating the retangle

GraniteElastic=np.loadtxt('GraniteElastic.txt')
interfaceElastic=np.loadtxt('interfaceElastic.txt')
#--------------------------------------------------------------------------------------material
for number in range(partNumbers):#here, all components are generated and material created, section assigned.
    main_PartGen.partCircleGen(CoarseAggregate[number],innerCircleData[number][0],innerCircleData[number][1],innerCircleData[number][2])
    main_PartGen.interfaceGen(interface[number],interfaceData[number][0],interfaceData[number][1],
        interfaceData[number][2],interfaceData[number][3])
    main_Property.materialCreate(CoarseAggregate[number],GraniteElastic[number],0.3)#property of rock
    main_Property.materialCreate(interface[number],interfaceElastic[number],0.3)
    main_Property.sectionCreate(CoarseAggregate[number],CoarseAggregate[number])
    main_Property.sectionCreate(interface[number],interface[number])
    main_Property.assignSection(CoarseAggregate[number],CoarseAggregate[number])
    main_Property.assignSection(interface[number],interface[number])

main_Property.materialCreate('MainPart',49,0.3)#property of mortar
main_Property.sectionCreate('MainPart','MainPart')
main_Property.assignSection('MainPart','MainPart')

#----------------------------------------------------------------------------------------assembly
main_PartAssem.partInst('MainPart')
map(main_PartAssem.partInst,CoarseAggregate)
map(main_PartAssem.partInst,interface)

#----------------------------------------------------------------------------------------interaction
for number in range(partNumbers):
    main_Interaction.creatingTie(interface[number],CoarseAggregate[number],innerCircleData[number][0],
        innerCircleData[number][1],innerCircleData[number][2],number)
    main_Interaction.creatingTie('MainPart',interface[number],interfaceData[number][0],
        interfaceData[number][1],interfaceData[number][2],number)


#---------------------------------------------------------------------------------------------step--------------------
stepNum=10

main_Step.createStep('Step-1','Initial')
for i in range(stepNum):
    main_Step.createStep('Step-'+str(i+2),'Step-'+str(i+1))

#---------------------------------------------------------------------------------------------Load
main_Load.setBoundary('MainPart',1)#set the boundary
for i in range(stepNum):
    main_Load.setLoad('MainPart',20000/stepNum,i+1)

#---------------------------------------------------------------------------------------------mesh
main_Mesh.Mesh('MainPart',2)

for number in range(partNumbers):
    main_Mesh.Mesh(CoarseAggregate[number],2)
    main_Mesh.Mesh(interface[number],0.5)
