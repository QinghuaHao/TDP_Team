from controller import Robot, DistanceSensor
"""得到球员，全部加载到control中"""

from controller import Robot
from RedGoalkeeper import GoalKeeper
robot = Robot()
robotName = robot.getName()
if robotName == ('Red_Goalkeeper'):
    robotController = GoalKeeper(robot)