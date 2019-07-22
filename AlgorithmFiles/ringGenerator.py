import numpy as np 

def innerCircleGenerator():
    outerCircleData=[]
    innerCircleData=[]
    ringData=[]

    outerCircleData=np.loadtxt('Circle.txt')
    circleNumbers=len(outerCircleData)
    
    for i in range(circleNumbers):
        innerCircleData.append((outerCircleData[i][0],outerCircleData[i][1],outerCircleData[i][2]-outerCircleData[i][2]/20,outerCircleData[i][3]))
        ringData.append((outerCircleData[i][0],outerCircleData[i][1],
            outerCircleData[i][2],outerCircleData[i][2]-outerCircleData[i][2]/20,outerCircleData[i][3]))
    np.savetxt('innerCircleData.txt',innerCircleData)
    np.savetxt('ringData.txt',ringData)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import circleGenerator
    innerCircleGenerator()
    fig = plt.figure(figsize=(6, 6), dpi=100)
    plt.axis([0, 150, 0, 150])
    outerCircleData=np.loadtxt('Circle.txt')
    innerCircleData=np.loadtxt('innerCircleData.txt')
    for i in range(len(outerCircleData)):  # draw module
        # "*" used for transfer three parameters in one
        circleGenerator.drawCircle(outerCircleData[i][0],outerCircleData[i][1],outerCircleData[i][2])
        circleGenerator.drawCircle(innerCircleData[i][0],innerCircleData[i][1],innerCircleData[i][2])
    plt.show()

# plt.savefig("D:/tcount
