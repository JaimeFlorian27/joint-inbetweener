#Add a joint in the middle of two other joints
#Created by Jaime Florian1

import maya.cmds as cmds
import math

joints = cmds.ls(selection= True, l = True, type = "joint")

if not joints:
    cmds.warning("Select a joint first")

if len(joints) == 1:
    children_jnt = cmds.listRelatives(children = True, f = True)
    print(children_jnt)
    if children_jnt is None:
       cmds.warning("Joint does not have children")
    else:
        children_jnt = children_jnt[0]
        radius = (cmds.getAttr("%s.radius" % joints[0]) + cmds.getAttr("%s.radius" % children_jnt) )/2
        inbetween_jnt= cmds.joint(rad= radius)
        cmds.delete(cmds.parentConstraint(joints[0], children_jnt, inbetween_jnt))
        cmds.parent(children_jnt,inbetween_jnt)
    
if len(joints) == 2:
    children = cmds.listRelatives(joints[0], children = True, f= True)
    if children is not None:
        if joints[1] not in children:
            cmds.warning("First joint must be a direct parent of the second joint")
        else:               
            cmds.select(joints[0])
            children_jnt = joints[1]
            radius = (cmds.getAttr("%s.radius" % joints[0]) + cmds.getAttr("%s.radius" % children_jnt) )/2
            inbetween_jnt= cmds.joint(rad= radius)
            cmds.delete(cmds.parentConstraint(joints[0], children_jnt, inbetween_jnt))
            cmds.parent(children_jnt,inbetween_jnt)
    else:
        cmds.warning("First joint must be a direct parent of the second joint")

if len(joints) > 2:
    cmds.warning("Select only one or two joints")