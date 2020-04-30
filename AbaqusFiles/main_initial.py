from abaqus import *
from abaqusConstants import *

from ModelModule import MyModel

def createModel(ModelName):
    MyModel._modelName=ModelName
    mdb.Model(name=MyModel._modelName, modelType=STANDARD_EXPLICIT)