import numpy as np 
import randomGenerator


def elasticGenerator(materialName,baseNumber,shapeNumber):
    circleData=np.loadtxt('Circle.txt')
    circleNumbers=len(circleData)

    ElasticData=[]
    for number in range(circleNumbers):
        ElasticNum=randomGenerator.weibullGenrator(shapeNumber,baseNumber)
        ElasticData.append(ElasticNum)

    np.savetxt(str(materialName)+'Elastic.txt',ElasticData)

def plasticGenerator(materialName,baseNumber,shapeNumber):
    circleData=np.loadtxt('Circle.txt')
    circleNumbers=len(circleData)

    plasticData=[]
    for number in range(circleNumbers):
        plasticNum=randomGenerator.weibullGenrator(shapeNumber,baseNumber)
        plasticData.append(plasticNum)

    np.savetxt(str(materialName)+'Plastic.txt',plasticData)

if __name__=='__main__':
    elasticGenerator('Granite',60000,10)
    elasticGenerator('interface',44000,1.5)