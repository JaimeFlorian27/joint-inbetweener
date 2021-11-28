#Add a joint in the middle of two other joints
#Created by Jaime Florian1

import maya.cmds as cmds
import maya.api.OpenMaya as om2
from functools import partial

def getSliderValue(slider):
    return cmds.floatSliderGrp(slider,q=1, v=1)

def setJointPosition(start_jnt,inbtwn_jnt,end_jnt,slider):
     w = getSliderValue(slider)
     print(w)
     start_jnt_v = om2.MVector(cmds.xform(start_jnt, q=True, t=True, ws=True))
     end_jnt_v = om2.MVector(cmds.xform(end_jnt, q=True, t=True,ws=True))
     inbtwn_jnt_v = (end_jnt_v-start_jnt_v) * w + start_jnt_v
     print(inbtwn_jnt_v)
     cmds.xform(inbtwn_jnt, t=list(inbtwn_jnt_v), ws= True)
     cmds.parent(end_jnt,inbtwn_jnt)
     cmds.select(inbtwn_jnt)

def insertMiddleJoint(slider, *args):

    #get the selected joints

    joints = cmds.ls(selection= True, l = True, type = "joint")

    #check if joints were selected

    if not joints:
        cmds.warning("Select a joint first")

    #If only one joint is selected
    if len(joints) == 1:
        #check if the joint has children, it must have children in order to work
        end_jnt = cmds.listRelatives(children = True, f = True)

        if end_jnt is None:
           cmds.warning("Joint does not have children")
        else:
            #get the first children from the joint
            end_jnt = end_jnt[0]
            #average the radius of the parent and children joint
            radius = (cmds.getAttr("%s.radius" % joints[0]) + cmds.getAttr("%s.radius" % end_jnt) )/2
            #create the inbetween joint (it is created as a children of the parent joint because it is still selected, it's one of the properties of the cmds.joint command)
            inbetween_jnt= cmds.joint(rad= radius)
            setJointPosition(joints[0],inbetween_jnt,end_jnt,slider)

    #if two joints are selected
    if len(joints) == 2:
        #get the children of the first joint
        children = cmds.listRelatives(joints[0], children = True, f= True)
        #if it has children
        if children is not None:
            #second joint has to be a direct children of the first one 
            if joints[1] not in children:
                cmds.warning("First joint must be a direct parent of the second joint")
            else:
                #select the first joint (in order to be set as a parent during the creation of the inbetween joint)               
                cmds.select(joints[0])
                #set the second joint from the initially selected as the end joint
                end_jnt = joints[1]
                radius = (cmds.getAttr("%s.radius" % joints[0]) + cmds.getAttr("%s.radius" % end_jnt) )/2
                inbetween_jnt= cmds.joint(rad= radius)
                setJointPosition(joints[0],inbetween_jnt,end_jnt,slider)
        else:
            cmds.warning("First joint must be a direct parent of the second joint")

    #if more than two joints are selected
    if len(joints) > 2:
        cmds.warning("Select only one or two joints")

    cmds.setFocus("MayaWindow")


#create window
mainWindow = cmds.window(t = "Joint Inbetweener", wh=(200,140), mxb=False)
layout = cmds.columnLayout(adjustableColumn=True, rs = 10)
separator_top = cmds.separator(st='none')
startEnd_label = cmds.text('Start-End position:', al='left')
positionFloatSlider = cmds.floatSliderGrp(min=-0.0, max=1.0, v=0.5, field = True)
insertButton = cmds.button(l = "Insert Joint", al = 'center', c= partial(insertMiddleJoint, positionFloatSlider))
cmds.setParent('..')
layout2 = cmds.rowLayout(nc=2, adj= True)
jointNumber_intField= cmds.intField(min = 2, max = 100, v=2)
insertMultiple_btn = cmds.button(label = 'Insert Joints')

cmds.showWindow(mainWindow)