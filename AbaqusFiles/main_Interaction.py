from abaqus import *
from abaqusConstants import *
import interaction

def creatingTie(MasterinstanceName,SlaveinstanceName,target_x,target_y,radi,order):
    a = mdb.models['Model-1'].rootAssembly
    s1 = a.instances[MasterinstanceName].edges
    side1Edges1 = s1.findAt(((target_x, target_y+radi, 0.0), ))
    region1=a.Surface(side1Edges=side1Edges1, name='m_Surf-'+MasterinstanceName+SlaveinstanceName+str(order))
    a = mdb.models['Model-1'].rootAssembly
    s1 = a.instances[SlaveinstanceName].edges
    side1Edges1 = s1.findAt(((target_x, target_y+radi, 0.0), ))
    region2=a.Surface(side1Edges=side1Edges1, name='s_Surf-'+SlaveinstanceName+MasterinstanceName+str(order))
    mdb.models['Model-1'].Tie(name='Constraint-'+MasterinstanceName+str(order), master=region1, slave=region2, 
        positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)