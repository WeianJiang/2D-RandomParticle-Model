import numpy as np


length=200
height=900

def drawCircle(centroid_x, centroid_y, radi):  # draw circles by given parameters, in which order is useless
    import matplotlib.pyplot as plt
    theta = np.arange(0, 2*np.pi, 0.01)
    x = centroid_x + radi * np.cos(theta)
    y = centroid_y + radi * np.sin(theta)
    plt.plot(x, y)


def boudaryDetect(x, y, r):  # Funtion used to detect whether the circle cross the boundry
    if x-r > 5 and y-r > 5 and x+r < length -5 and y+r < height-5:
        return True


# Function to detect the position relatioship between two circles
def overlapDetect(x1, y1, r1, x2, y2, r2):
    distanceSquare = np.square(x1-x2)+np.square(y1-y2)
    if distanceSquare  < (r1+r2)**2 +50:
        return True  # return ture if overlap


def dataGen(minimumRadi,maximumRadi):  # generate parameters of circle
    centroid_x = np.random.rand()*length
    centroid_y = np.random.rand()*height
    radi = np.random.uniform(minimumRadi, maximumRadi)
    if boudaryDetect(centroid_x, centroid_y, radi):
        return [centroid_x, centroid_y, radi]
    else:
        return dataGen(minimumRadi,maximumRadi)


def areaRatio(circleArray):
    area=0
    for i in range(len(circleArray)):
        area = 3.14*circleArray[i][2]**2 + area
    return area/length/height


def overlapCounting(circleArray):
    count = 0
    for k in range(len(circleArray)):  # a checking module
        for j in range(k+1, len(circleArray)):
            if overlapDetect(circleArray[k][0], circleArray[k][1], circleArray[k][2], circleArray[j][0], circleArray[j][1], circleArray[j][2]):
                count += 1
                #print False
            else:
                pass
    return count


def circleGenerator(trialTimes,minimumRadi,maximumRadi,circleData=[]):
    if len(circleData)==0:
        circleData.append(dataGen(minimumRadi,maximumRadi))
        formerLength=0
    else:
        formerLength=len(circleData)
    for number in range(trialTimes):
        newCircle = dataGen(minimumRadi,maximumRadi)
        looptimes = 0
        for i in range(len(circleData)):
            if overlapDetect(newCircle[0], newCircle[1], newCircle[2], circleData[i][0], circleData[i][1], circleData[i][2]):
                break
            looptimes += 1
        if looptimes == len(circleData):
            circleData.append(newCircle)
    for order in range(formerLength,len(circleData)):
        circleData[order].append(order)
    return circleData







if __name__ == "__main__":
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(length/50, height/50), dpi=100)
    plt.axis([0, length, 0, height])
    #print dataGen()
    ratio=0
    while ratio<0.4:

        circleData=circleGenerator(200,8,10)
        circleData=circleGenerator(10000,5,8,circleData)
        circleData=np.array(circleData)
        np.savetxt('Circle.txt',circleData)
        ratio=areaRatio(circleData)

    circleData=np.loadtxt('Circle.txt')
    # with open('file.txt','w') as f:
    #     f.write(str(circleData))
    import materialGenerator
    #materialGenerator.ElasticGenerator('Granite',60)
    #print overlapCounting(circleData)
    print(areaRatio(circleData))
    for i in range(len(circleData)):  # draw module
        # "*" used for transfer three parameters in one
        drawCircle(circleData[i][0],circleData[i][1],circleData[i][2])
    plt.show()

# plt.savefig("D:/tcount
