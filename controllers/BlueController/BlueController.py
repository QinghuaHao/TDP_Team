"""
Blue Team Main Controller.
This controller should be selected as controller for Blue team robots.
Roles will be assigned automatically for each robot.
"""

from controller import Robot
from BlueGoalkeeper import Goalkeeper
from BlueStriker import Defender
from BlueDefencer1 import ForwardLeft
from BlueDefencer2 import ForwardRight

# Create the Robot instance.
robot = Robot()
# Get the Robot Name to find the role.
robotName = robot.getName()

# Compare the Robot Name and assign the role.
if robotName == "Blue_Goalkeeper":
    robotController = Goalkeeper(robot)
elif robotName == "Blue_Striker_1":
    robotController = Defender(robot)
elif robotName == "Blue_Defender_1":
    robotController = ForwardLeft(robot)
else:
    robotController = ForwardRight(robot)

# Run the Robot Controller.
robotController.run()