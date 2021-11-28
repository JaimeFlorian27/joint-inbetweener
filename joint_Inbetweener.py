# Add a joint in the middle of two other joints
# Created by Jaime Florian

import maya.cmds as cmds
import maya.api.OpenMaya as om2
from functools import partial


def getSliderValue(slider):
    return cmds.floatSliderGrp(slider, q=1, v=1)


def setJointPosition(start_jnt, inbtwn_jnt, end_jnt, w):
    print(w)
    # positions
    start_jnt_v = om2.MVector(cmds.xform(start_jnt, q=True, t=True, ws=True))
    end_jnt_v = om2.MVector(cmds.xform(end_jnt, q=True, t=True, ws=True))

    # rotations
    start_jnt_v_rot = om2.MVector(cmds.xform(start_jnt, q=True, ro=True, ws=True))
    end_jnt_v_rot = om2.MVector(cmds.xform(end_jnt, q=True, ro=True, ws=True))

    # get position
    inbtwn_jnt_v = (end_jnt_v - start_jnt_v) * w + start_jnt_v
    # get rotation
    inbtwn_jnt_v_rot = (end_jnt_v_rot - start_jnt_v_rot) * w + start_jnt_v_rot

    # set position
    cmds.xform(inbtwn_jnt, t=inbtwn_jnt_v, ws=True)

    # set rotation
    #cmds.xform(inbtwn_jnt, ro=inbtwn_jnt_v_rot, ws=True)

    #freeze rotations
    #cmds.makeIdentity(a=True, r = True)

    cmds.parent(end_jnt, inbtwn_jnt)
    cmds.select(inbtwn_jnt)

def insertMiddleJoints(type,*args):
    # get the selected joints

    joints = cmds.ls(selection=True, l=True, type="joint")

    # check if joints were selected

    if not joints:
        cmds.warning("Select a joint first")

    # If only one joint is selected
    if len(joints) == 1:
        # check if the joint has children, it must have children in order to work
        end_jnt = cmds.listRelatives(children=True, f=True)

        if end_jnt is None:
            cmds.warning("Joint does not have children")
        else:
            # get the first children from the joint
            end_jnt = end_jnt[0]
            w = 0
            if (type == 1):
                jointsNumber = cmds.intField(jointNumber_intField, q=1, v=1)
                for i in range(0, jointsNumber):
                    if i > 0:
                        end_jnt = cmds.listRelatives(inbetween_jnt, children=True, f=True)[0]
                    w = w + 1 / float(jointsNumber + 1)
                    radius = (cmds.getAttr("%s.radius" % joints[0]) + cmds.getAttr("%s.radius" % end_jnt)) / 2

                    # create the inbetween joint (it is created as a children of the parent joint because it is still selected, it's one of the properties of the cmds.joint command)

                    inbetween_jnt = cmds.joint(rad=radius)
                    setJointPosition(joints[0], inbetween_jnt, end_jnt, w)
            else:    
                jointsNumber = 1
                for i in range(0, jointsNumber):
                    if i > 0:
                        end_jnt = cmds.listRelatives(inbetween_jnt, children=True, f=True)[0]
                    w = getSliderValue(positionFloatSlider)
                    radius = (cmds.getAttr("%s.radius" % joints[0]) + cmds.getAttr("%s.radius" % end_jnt)) / 2

                    # create the inbetween joint (it is created as a children of the parent joint because it is still selected, it's one of the properties of the cmds.joint command)

                    inbetween_jnt = cmds.joint(rad=radius)
                    setJointPosition(joints[0], inbetween_jnt, end_jnt, w)


    # if two joints are selected
    if len(joints) == 2:
        # get the children of the first joint
        children = cmds.listRelatives(joints[0], children=True, f=True)
        # if it has children
        if children is not None:
            # second joint has to be a direct children of the first one
            if joints[1] not in children:
                cmds.warning("First joint must be a direct parent of the second joint")
            else:
                # select the first joint (in order to be set as a parent during the creation of the inbetween joint)
                cmds.select(joints[0])
                # set the second joint from the initially selected as the end joint
                end_jnt = joints[1]
                w=0
                if (type == 1):
                    jointsNumber = cmds.intField(jointNumber_intField, q=1, v=1)
                    for i in range(0, jointsNumber):
                        if i > 0:
                            end_jnt = cmds.listRelatives(inbetween_jnt, children=True, f=True)[0]
                        w = w + 1 / float(jointsNumber + 1)
                        radius = (cmds.getAttr("%s.radius" % joints[0]) + cmds.getAttr("%s.radius" % end_jnt)) / 2

                        # create the inbetween joint (it is created as a children of the parent joint because it is still selected, it's one of the properties of the cmds.joint command)

                        inbetween_jnt = cmds.joint(rad=radius)
                        setJointPosition(joints[0], inbetween_jnt, end_jnt, w)
                else:    
                    jointsNumber = 1
                    for i in range(0, jointsNumber):
                        if i > 0:
                            end_jnt = cmds.listRelatives(inbetween_jnt, children=True, f=True)[0]
                        w = getSliderValue(positionFloatSlider)
                        radius = (cmds.getAttr("%s.radius" % joints[0]) + cmds.getAttr("%s.radius" % end_jnt)) / 2

                        # create the inbetween joint (it is created as a children of the parent joint because it is still selected, it's one of the properties of the cmds.joint command)

                        inbetween_jnt = cmds.joint(rad=radius)
                        setJointPosition(joints[0], inbetween_jnt, end_jnt, w)
        else:
            cmds.warning("First joint must be a direct parent of the second joint")

    # if more than two joints are selected
    if len(joints) > 2:
        cmds.warning("Select only one or two joints")

    cmds.setFocus("MayaWindow")

# create window

mainWindow = cmds.window(t="Joint Inbetweener", wh=(200, 140), mxb=False)
tab_layout = cmds.tabLayout()
singleJnt_clmnLayout = cmds.columnLayout(adjustableColumn=True, rs=10)
separator_top = cmds.separator(st="none")
startEnd_label = cmds.text("Start-End position:", al="left")
positionFloatSlider = cmds.floatSliderGrp(min=-0.0, max=1.0, v=0.5, field=True)
insertButton = cmds.button(
    l="Insert Joint", al="center", c=partial(insertMiddleJoints, 0)
)
cmds.setParent("..")
multipleJnt_clmnLayout = cmds.columnLayout(adjustableColumn=True, rs=10)
multipleJnt_label = cmds.text("Number of Joints:", al="left")
layout2 = cmds.rowLayout(nc=2, adj=True)
separator_top = cmds.separator(st="none")
jointNumber_intField = cmds.intField(min=2, max=100, v=2)
cmds.setParent("..")
insertMultiple_btn = cmds.button(label="Insert Joints", c=partial(insertMiddleJoints, 1))
cmds.setParent("..")

cmds.tabLayout(tab_layout, e=1, tl = ((singleJnt_clmnLayout, 'Single Joint'),(multipleJnt_clmnLayout, 'Multiple Joints')))
cmds.showWindow(mainWindow)
