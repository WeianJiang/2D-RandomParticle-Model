import numpy as np 
import randomGenerator
from randomGenerator import weibullGenrator


def elasticGenerator(materialName,baseNumber,shapeNumber):
    circleData=np.loadtxt('Circle.txt')
    circleNumbers=len(circleData)

    ElasticData=[]
    for number in range(circleNumbers):
        ElasticNum=weibullGenrator(shapeNumber,baseNumber)
        ElasticData.append(ElasticNum)

    np.savetxt(str(materialName)+'Elastic.txt',ElasticData)

def plasticGenerator(materialName,baseNumber,shapeNumber):
    circleData=np.loadtxt('Circle.txt')
    circleNumbers=len(circleData)

    plasticData=[]
    for number in range(circleNumbers):
        plasticNum=weibullGenrator(shapeNumber,baseNumber)
        plasticData.append(plasticNum)

    np.savetxt(str(materialName)+'Plastic.txt',plasticData)


def meshComPlasticityGenerator(materialNumbers,baseNumber,shapeNumber):
    materialArray=np.zeros((materialNumbers,6))
    for i in range(materialNumbers):

        fct=weibullGenrator(shapeNumber,baseNumber) # the given ultimate strength
        materialArray[i][0]=fct
        materialArray[i][1]=0.002-0.002

        materialArray[i][2]=0.2*fct
        materialArray[i][3]=0.006-0.002

        materialArray[i][4]=0.2*fct
        materialArray[i][5]=0.05-0.002
    ComDamageArray=np.zeros((materialNumbers,6))
    for i in range(materialNumbers):
        ComDamageArray[i][0]=0
        ComDamageArray[i][1]=0

        ComDamageArray[i][2]=0.01355
        ComDamageArray[i][3]=materialArray[i][3]

        ComDamageArray[i][4]=0.9238
        ComDamageArray[i][5]=materialArray[i][5]

    np.savetxt('ComMeshPl.txt',materialArray)
    np.savetxt('ComDamage.txt',ComDamageArray)

def meshTenPlasticityGenerator(materialNumbers,baseNumber,shapeNumber):
    materialArray=np.zeros((materialNumbers,6))
    for i in range(materialNumbers):

        fct=weibullGenrator(shapeNumber,baseNumber) # the given ultimate strength
        materialArray[i][0]=fct
        materialArray[i][1]=0.00015-0.00015

        materialArray[i][2]=0.2*fct
        materialArray[i][3]=0.0003-0.00015

        materialArray[i][4]=0.2*fct
        materialArray[i][5]=0.005-0.00015

    TenDamageArray=np.zeros((materialNumbers,6))
    for i in range(materialNumbers):
        
        TenDamageArray[i][0]=0
        TenDamageArray[i][1]=0

        TenDamageArray[i][2]=0.9
        TenDamageArray[i][3]=materialArray[i][3]

        TenDamageArray[i][4]=0.97
        TenDamageArray[i][5]=materialArray[i][5]

    np.savetxt('TenMeshPl.txt',materialArray)
    np.savetxt('TenDamage.txt',TenDamageArray)

if __name__=='__main__':
    elasticGenerator('Granite',60000,10)
    elasticGenerator('interface',44000,1.5)
    meshComPlasticityGenerator(10,40,2)
    meshTenPlasticityGenerator(10,8,5)