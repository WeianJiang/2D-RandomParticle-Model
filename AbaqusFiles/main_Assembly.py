from abaqus import *
from abaqusConstants import *

from AbaqusFiles.Components.SteelBar import SteelBar_module

from ModelModule import MyModel


class AssemblyModule(MyModel):

    def partInst(self):
        a = mdb.models[MyModel._modelName].rootAssembly
        a.DatumCsysByDefault(CARTESIAN)
        p = mdb.models[MyModel._modelName].parts[MyModel._concretePartName]
        a.Instance(name=MyModel._concretePartName, part=p, dependent=ON)

        

    def partTranslate(self,InstanceName,target_x,target_y):
        a = mdb.models[MyModel._modelName].rootAssembly
        a.translate(instanceList=(InstanceName, ), vector=(target_x,target_y, 0.0))
        #: The instance Part-49 was translated by 500.E-03, 0., 0. with respect to the assembly coordinate system