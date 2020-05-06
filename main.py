# from AbaqusFiles import main_PartGen
# from AbaqusFiles import main_Property
# from AbaqusFiles import main_PartAssem
# from AbaqusFiles import main_Interaction
# from AbaqusFiles import main_Load
# from AbaqusFiles import main_Mesh
# from AbaqusFiles import main_Step
# from AbaqusFiles import main_Job
# import numpy as np

from AlgorithmFiles import dspLoad


Model=dspLoad.dspLoad()
Model.setSize(200,900)
Model.setPath(4,'200900-1')
Model.setLoadDsp(-50)


# def createMeshModel(ModelPath=1,size=150,Load=-0.2,Job_name='Job-Test'):
#     MeshModel=MeshPartModel.MeshPartModel()
#     MeshModel.setSize(size)
#     MeshModel.setPath(ModelPath)
#     MeshModel.setLoadDsp(Load)
#     MeshModel.setJobName(Job_name)


# #------------------------------------------------------------------------------------importing data
# circleData = np.loadtxt('ModelInfoFiles/1/Circle.txt')
# interfaceData=np.loadtxt('ModelInfoFiles/1/ringData.txt')#load the interface data
# innerCircleData=np.loadtxt('ModelInfoFiles/1/innerCircleData.txt')
# CoarseAggregate=[]
# interface=[]
# partNumbers=len(circleData)
# for number in range(partNumbers):
#     CoarseAggregate.append('CoarseAggregate-'+str(number))
#     interface.append('interface-'+str(number))
# #---------------------------------------------------------------------------------------part------------------------
# main_PartGen.partRectGen('MainPart',circleData)#generating the retangle

# GraniteElastic=np.loadtxt('ModelInfoFiles/1/GraniteElastic.txt')
# interfaceElastic=np.loadtxt('ModelInfoFiles/1/interfaceElastic.txt')
# #--------------------------------------------------------------------------------------material
# for number in range(partNumbers):#here, all components are generated and material created, section assigned.
#     main_PartGen.partCircleGen(CoarseAggregate[number],innerCircleData[number][0],innerCircleData[number][1],innerCircleData[number][2])
#     main_PartGen.interfaceGen(interface[number],interfaceData[number][0],interfaceData[number][1],
#         interfaceData[number][2],interfaceData[number][3])
#     main_Property.materialCreate(CoarseAggregate[number],GraniteElastic[number],0.3,2.7e-09)#property of rock
#     main_Property.materialCreate(interface[number],interfaceElastic[number],0.3,2e-09)
#     main_Property.sectionCreate(CoarseAggregate[number],CoarseAggregate[number])
#     main_Property.sectionCreate(interface[number],interface[number])
#     main_Property.assignSection(CoarseAggregate[number],CoarseAggregate[number])
#     main_Property.assignSection(interface[number],interface[number])

# main_Property.materialCreate('MainPart',23000,0.2,2e-09)#property of mortar
# main_Property.PLassign('MainPart')
# main_Property.sectionCreate('MainPart','MainPart')
# main_Property.assignSection('MainPart','MainPart')

# #----------------------------------------------------------------------------------------assembly
# main_PartAssem.partInst('MainPart')
# map(main_PartAssem.partInst,CoarseAggregate)
# map(main_PartAssem.partInst,interface)

# #----------------------------------------------------------------------------------------interaction
# for number in range(partNumbers):
#     main_Interaction.creatingTie(interface[number],CoarseAggregate[number],innerCircleData[number][0],
#         innerCircleData[number][1],innerCircleData[number][2],number)
#     main_Interaction.creatingTie('MainPart',interface[number],interfaceData[number][0],
#         interfaceData[number][1],interfaceData[number][2],number)


# #---------------------------------------------------------------------------------------------step--------------------
# stepNum=1

# main_Step.createStep('Step-1','Initial')
# if stepNum>1:
#     for i in range(stepNum):
#         if i+2<=stepNum:
#             main_Step.createStep('Step-'+str(i+2),'Step-'+str(i+1))



# #---------------------------------------------------------------------------------------------Load
# main_Load.setBoundary('MainPart',1)#set the boundary
# index=main_Load.setReferPoint()

# dsp=-0
# for i in range(stepNum):
# #     main_Load.setLoad('MainPart',6000/stepNum,i+1)
#     # main_Load.setReferConLoad(-6500/stepNum,i+1,index)
#     dsp=-0.2/stepNum+dsp
#     #main_Load.setDspLoad('MainPart',dsp,i+1)
#     main_Load.setReferDspLoad('MainPart',dsp,i+1,index)




# #---------------------------------------------------------------------------------------------mesh
# main_Mesh.Mesh('MainPart',2)

# for number in range(partNumbers):
#     main_Mesh.Mesh(CoarseAggregate[number],2)
#     #main_Mesh.Mesh(interface[number],interfaceData[number][3]/10/2)
#     main_Mesh.Mesh(interface[number],2)


# #----------------------------------------------------------------------Job
# #main_Job.creatJob('Job-dsp',1)