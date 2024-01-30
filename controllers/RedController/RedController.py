from controller import Robot, DistanceSensor
"""得到球员，全部加载到control中"""
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from controller import Robot
import RedGoalkeeper
robot = Robot()
robotName = robot.getName()
if robotName == ('Red_Goalkeeper'):
    robotController = RedGoalkeeper.GoalKeeper(robot)