import numpy as np 
import randomGenerator


def ElasticGenerator(materialName,baseNumber):
    circleData=np.loadtxt('Circle.txt')
    circleNumbers=len(circleData)

    ElasticData=[]
    for number in range(circleNumbers):
        ElasticNum=randomGenerator.weibullGenrator(10,baseNumber)
        ElasticData.append(ElasticNum)

    np.savetxt(str(materialName)+'Elastic.txt',ElasticData)



if __name__=='__main__':
    ElasticGenerator('Granite',60000)
    ElasticGenerator('interface',44000)