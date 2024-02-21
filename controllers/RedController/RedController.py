
"""得到球员，全部加载到control中"""
import sys
sys.path.append(".")
sys.path.append("..")

from controller import Robot
from RedGoalKeeper import GoalKeeper
from RedDefender1 import DefenderLeft
from RedDefender2 import DefenderRight
from RedStriker1 import Forward
robot = Robot()
robotName = robot.getName()
if robotName == ('Red_Goalkeeper'):
    robotController = GoalKeeper(robot)
elif robotName==('Red_Defender_1'):
    robotController = DefenderLeft(robot)
elif robotName==('Red_Defender_2'):
    robotController = DefenderRight(robot)
elif robotName==('Red_Striker_1'):
    robotController = Forward(robot)
   
robotController.run()