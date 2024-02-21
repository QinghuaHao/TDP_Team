"""
防守队员1和2相同逻辑
1.只要丢球就找球
2.基准状态，无人无球时，防后
3.球不在我方半场，敌人却在防守区
4.球在我方半场，防止射门
进入防守区域，上去抢球
判断是否足够近
敌人远，瞄准传球
敌人很近，逼近解围
"""
"""
Red Team Right Defender robot behaviours.
"""
import sys
sys.path.append(".")
sys.path.append("..")
from InitRobot import SoccerRobot
from GlobalConstant import TIME_STEP,LoadMoveFile
import BasicFunction
import RedTeamStrategy


class DefenderRight(SoccerRobot):
    def run(self):
        self.printSelf()
        while self.robot.step(TIME_STEP) != -1:

            if self.isNewBallDataValuable():

                # Do not remove this!
                # ----------------------
                self.getsupervisorData()
                # ----------------------

                # Use the ballData (location) to do something.
                ballCoordinate = self.getBallData()
                # print("RedDefenderRight - ballCoordinate: ", ballCoordinate)
                selfCoordinate = self.getselfPostiton()
                # print("RedDefenderRight - selfCoordinate: ", selfCoordinate)
                decidedMotion = self.decidedMotion(ballCoordinate, selfCoordinate)
                # print("RedDefenderRight - decidedMotion: ", decidedMotion.Name)
                if self.isNewMotionValuable(decidedMotion):
                    forwardsSprintInterrupt = self.currentMoving and (
                                self.currentMoving.name == self.motions.ForwardsSprint.name and decidedMotion.name != self.motions.ForwardsSprint.name)

                    # interruptCheck = self.currentlyMoving and\
                    #          (self.currentlyMoving.name == self.motions.turnLeft40.name and decidedMotion.name != self.motions.turnLeft40.name and\
                    #           decidedMotion.name != self.motions.sideStepLeft.name and decidedMotion.name != self.motions.sideStepRight.name) or\
                    #          (self.currentlyMoving.name == self.motions.turnRight40.name and decidedMotion.name != self.motions.turnRight40.name)

                    leftShootCheck = self.currentMoving and self.currentMoving.name == self.motions.RightShoot.name and self.currentMoving.isOver() and decidedMotion.name == self.motions.RightShoot.name

                    # if interruptCheck:
                    #   self.interruptMotion()
                    # if forwardsSprintInterrupt:
                    #   self.interruptForwardsSprint()
                    # print("RedDefenderRight - Motion interrupted!")
                    self.clearMotionList()
                    # if interruptCheck:
                    #   self.addMotionToQueue(self.motions.standInit)
                    if leftShootCheck:
                        self.loadMotionToList(self.motions.shoot)
                    else:
                        self.loadMotionToList(decidedMotion)

                self.startMotion()
            else:

                # It seems there is a problem.
                # print("NO BALL DATA!!!")
                pass

    # Override decideMotion
    def decidedMotion(self, ballCoordinate, selfCoordinate):

        # Check the goal scored to balance itself.
        if self.checkGetScore() == 1:
            return self.motions.HandWave
        elif self.checkGetScore() == -1:
            return self.motions.StandInit

        # Fall Detection
        robotHeightFromGround = self.getselfPostiton()[2]
        if robotHeightFromGround < 0.2:
            if self.getleftsonarDistance() == 2.55 and self.getrightsonarDistance() == 2.55:
                return self.motions.standUpFromBack
            else:
                return self.motions.standUpFromFront

        # Check the oponent has ball priority.
        if self.checkBallpriority() == "B":
            return self.motions.standInit

        # We are going to use these values to check if there is an obstacle in front of the robot.
        leftDistance = self.getleftsonarDistance()
        rightDistance = self.getrightsonarDistance()

        robotHeadingAngle = self.getRollPitchYaw()[2]

        # If the ball on the opponent field.
        if RedTeamStrategy.getZone(ballCoordinate) > 9:

            # If the ball on team member.
            if self.knowBallOwner()[0] == "R" and self.knowBallOwner() != "RedDefender2":

                # Go to zone 15.
                if RedTeamStrategy.getZone(selfCoordinate) != 15:
                    # print("I am going to 15")
                    # Bottom line of zone 15.
                    zoneTargetX = (RedTeamStrategy.PLAY_ZONE[15][0][0] + RedTeamStrategy.PLAY_ZONE[15][1][0]) / 2
                    zoneTargetY = RedTeamStrategy.PLAY_ZONE[15][0][1]
                    # Find the angle between the target zone and robot heading.
                    turningAngle = BasicFunction.calculateTurnAngle([zoneTargetX, zoneTargetY],
                                                                                          selfCoordinate,
                                                                                          robotHeadingAngle)
                    turningMotion = self.getTurnMotion(turningAngle)
                    if turningMotion is not None:
                        return turningMotion

                    # Check if there is an obstacle in front of the robot.
                    if self.obstacleAvoidance:
                        if leftDistance < 0.75:
                            return self.motions.SideStepRight
                        elif rightDistance < 0.75:
                            return self.motions.SideStepLeft

                    if self.currentMoving and self.currentMoving.name == "ForwardsSprint" and self.currentMoving.getTime() == 1360:  # we reached the end of forward.motion
                        self.currentMoving.setTime(360)  # loop back to the beginning of the walking sequence

                    return self.motions.ForwardsSprint

                # Head to ball.
                else:
                    # print("I am waiting on 15")
                    # Find the angle between the ball and robot heading.
                    turningAngle = BasicFunction.calculateTurnAngle(ballCoordinate,
                                                                                          selfCoordinate,
                                                                                          robotHeadingAngle)
                    turningMotion = self.getTurnMotion(turningAngle)
                    if turningMotion is not None:
                        return turningMotion

            # If the ball on the opponent.
            elif self.knowBallOwner()[0] == "B":

                # Go to zone 6.
                if RedTeamStrategy.getZone(selfCoordinate) != 6:
                    # print("I am going to 6")
                    # Bottom line of zone 6.
                    zoneTargetX = (RedTeamStrategy.PLAY_ZONE[6][0][0] + RedTeamStrategy.PLAY_ZONE[6][1][0]) / 2
                    zoneTargetY = RedTeamStrategy.PLAY_ZONE[6][0][1]
                    # Find the angle between the target zone and robot heading.
                    turningAngle = BasicFunction.calculateTurnAngle([zoneTargetX, zoneTargetY],
                                                                                          selfCoordinate,
                                                                                          robotHeadingAngle)
                    turningMotion = self.getTurnMotion(turningAngle)
                    if turningMotion is not None:
                        return turningMotion

                    # Check if there is an obstacle in front of the robot.
                    if self.obstacleAvoidance:
                        if leftDistance < 0.75:
                            return self.motions.sideStepRight
                        elif rightDistance < 0.75:
                            return self.motions.sideStepLeft

                    if self.currentMoving and self.currentMoving.name == "ForwardsSprint" and self.currentMoving.getTime() == 1360:  # we reached the end of forward.motion
                        self.currentMoving.setTime(360)  # loop back to the beginning of the walking sequence

                    return self.motions.ForwardsSprint

                # Head to ball.
                else:
                    # print("I am waiting on 6")
                    # Find the angle between the ball and robot heading.
                    turningAngle = BasicFunction.calculateTurnAngle(ballCoordinate,
                                                                                          selfCoordinate,
                                                                                          robotHeadingAngle)
                    turningMotion = self.getTurnMotion(turningAngle)
                    if turningMotion is not None:
                        return turningMotion

            # The ball on the robot itself
            else:
                # print("I am going to press")
                # Find the angle between the ball and robot heading.
                turningAngle = BasicFunction.calculateTurnAngle(ballCoordinate, selfCoordinate,
                                                                                      robotHeadingAngle)
                turningMotion = self.getTurnMotion(turningAngle)
                if turningMotion is not None:
                    return turningMotion

                bodyDistanceFromBall = BasicFunction.calculateDistance(ballCoordinate, selfCoordinate)

                # Decide wehere to shoot or pass.
                if bodyDistanceFromBall < 0.25:
                    #  We have to look for the distance from left foot becuase or robots are left footed.

                    # If the robot at the 16th or 18th zones, the goal is 17th zone.
                    if RedTeamStrategy.getZone(ballCoordinate) == 16 or RedTeamStrategy.getZone(
                            ballCoordinate) == 18:
                        turningAngleForGoalLeft = BasicFunction.calculateTurnAngle(
                            [RedTeamStrategy.PLAY_ZONE[17][0][0], 0], selfCoordinate, robotHeadingAngle)
                        turningAngleForGoalRight = BasicFunction.calculateTurnAngle(
                            [RedTeamStrategy.PLAY_ZONE[17][1][0], 0], selfCoordinate, robotHeadingAngle)

                    # Else, shoot to goal!
                    else:
                        # If decided to shoot
                        # We have to calculate the goal angle and sideSteps according to this angle.
                        turningAngleForGoalLeft = BasicFunction.calculateTurnAngle(
                            RedTeamStrategy.BLUE_GOAL["Left"], selfCoordinate, robotHeadingAngle)
                        turningAngleForGoalRight = BasicFunction.calculateTurnAngle(
                            RedTeamStrategy.BLUE_GOAL["Right"], selfCoordinate, robotHeadingAngle)

                    if (turningAngleForGoalLeft > 0 and turningAngleForGoalRight > 0):
                        if turningAngleForGoalLeft < 76 or turningAngleForGoalRight < 76:
                            return self.motions.SidePass_Right
                        return self.motions.SideStepRight
                    elif (turningAngleForGoalLeft < 0 and turningAngleForGoalRight < 0):
                        if turningAngleForGoalLeft > -76 or turningAngleForGoalRight > -76:
                            return self.motions.SidePass_Left
                        return self.motions.SideStepLeft
                    elif (abs(turningAngleForGoalLeft) > 90 and abs(turningAngleForGoalRight) > 90):
                        if abs(turningAngleForGoalLeft) > abs(turningAngleForGoalRight):
                            return self.motions.SideStepLeft
                        else:
                            return self.motions.SideStepLeft
                    else:
                        if bodyDistanceFromBall < 0.2:
                            return self.motions.RightShoot
                        else:
                            return self.motions.ForwardsSprint

                # Check if there is an obstacle in front of the robot.
                elif self.obstacleAvoidance and leftDistance < bodyDistanceFromBall:
                    if leftDistance < 0.5:
                        return self.motions.SideStepRight
                    elif rightDistance < 0.5:
                        return self.motions.SideStepLeft

                if self.currentMoving and self.currentMoving.name == "ForwardsSprint" and self.currentMoving.getTime() == 1360:  # we reached the end of forward.motion
                    self.currentMoving.setTime(360)  # loop back to the beginning of the walking sequence

                return self.motions.ForwardsSprint

        # The ball on right or middle zone field.
        elif RedTeamStrategy.getZone(ballCoordinate) == 3 or RedTeamStrategy.getZone(
                ballCoordinate) == 6 or RedTeamStrategy.getZone(ballCoordinate) == 9 or \
                RedTeamStrategy.getZone(ballCoordinate) == 2 or RedTeamStrategy.getZone(
            ballCoordinate) == 5 or RedTeamStrategy.getZone(ballCoordinate) == 8:

            # If the ball on team member.
            if self.knowBallOwner()[0] == "R" and self.knowBallOwner() != "RedDefender2" and self.knowBallOwner() != "RedGoalKeeper":

                # Go to zone 9.
                if RedTeamStrategy.getZone(selfCoordinate) != 9:
                    # print("I am going to 9")
                    # Bottom line of zone 9.
                    zoneTargetX = (RedTeamStrategy.PLAY_ZONE[9][0][0] + RedTeamStrategy.PLAY_ZONE[9][1][0]) / 2
                    zoneTargetY = RedTeamStrategy.PLAY_ZONE[9][0][1]
                    # Find the angle between the target zone and robot heading.
                    turningAngle = BasicFunction.calculateTurnAngle([zoneTargetX, zoneTargetY],
                                                                                          selfCoordinate,
                                                                                          robotHeadingAngle)
                    turningMotion = self.getTurnMotion(turningAngle)
                    if turningMotion is not None:
                        return turningMotion

                    # Check if there is an obstacle in front of the robot.
                    if self.obstacleAvoidance:
                        if leftDistance < 0.75:
                            return self.motions.SideStepRight
                        elif rightDistance < 0.75:
                            return self.motions.SideStepLeft

                    if self.clearMotionList() and self.clearMotionList().name == "ForwardsSprint" and self.clearMotionList().getTime() == 1360:  # we reached the end of forward.motion
                        self.clearMotionList().setTime(360)  # loop back to the beginning of the walking sequence

                    return self.motions.ForwardsSprint

                # Head to ball.
                else:
                    # print("I am waiting on 9")
                    # Find the angle between the ball and robot heading.
                    turningAngle = BasicFunction.calculateTurnAngle(ballCoordinate,
                                                                                          selfCoordinate,
                                                                                          robotHeadingAngle)
                    turningMotion = self.getTurnMotion(turningAngle)
                    if turningMotion is not None:
                        return turningMotion

            # The ball on the opponent or on the robot itself.
            else:
                # print("I am going to press")
                # Find the angle between the ball and robot heading.
                turningAngle = BasicFunction.calculateTurnAngle(ballCoordinate, selfCoordinate,
                                                                                      robotHeadingAngle)
                turningMotion = self.getTurnMotion(turningAngle)
                if turningMotion is not None:
                    return turningMotion

                bodyDistanceFromBall = BasicFunction.calculateDistance(ballCoordinate, selfCoordinate)

                # Decide wehere to shoot or pass.
                if bodyDistanceFromBall < 0.25:
                    #  We have to look for the distance from left foot becuase or robots are left footed.

                    # The goal is the 11th zone. Passing...
                    turningAngleForGoalLeft = BasicFunction.calculateTurnAngle(
                        [RedTeamStrategy.PLAY_ZONE[11][0][1], RedTeamStrategy.PLAY_ZONE[11][1][0]], selfCoordinate,
                        robotHeadingAngle)
                    turningAngleForGoalRight = BasicFunction.calculateTurnAngle(
                        [RedTeamStrategy.PLAY_ZONE[11][0][0], RedTeamStrategy.PLAY_ZONE[11][1][1]], selfCoordinate,
                        robotHeadingAngle)

                    if (turningAngleForGoalLeft > 0 and turningAngleForGoalRight > 0):
                        if turningAngleForGoalLeft < 76 or turningAngleForGoalRight < 76:
                            return self.motions.SidePass_Right
                        return self.motions.SideStepRight
                    elif (turningAngleForGoalLeft < 0 and turningAngleForGoalRight < 0):
                        if turningAngleForGoalLeft > -76 or turningAngleForGoalRight > -76:
                            return self.motions.SidePass_Left
                        return self.motions.SideStepLeft
                    elif (abs(turningAngleForGoalLeft) > 90 and abs(turningAngleForGoalRight) > 90):
                        if abs(turningAngleForGoalLeft) > abs(turningAngleForGoalRight):
                            return self.motions.SideStepLeft
                        else:
                            return self.motions.SideStepRight
                    else:
                        if bodyDistanceFromBall < 0.2:
                            return self.motions.RightShoot
                        else:
                            return self.motions.ForwardsSprint

                # Check if there is an obstacle in front of the robot.
                elif self.obstacleAvoidance and leftDistance < bodyDistanceFromBall:
                    if leftDistance < 0.5:
                        return self.motions.SideStepRight
                    elif rightDistance < 0.5:
                        return self.motions.SideStepLeft

                if self.currentMoving and self.currentMoving.name == "forwardsSprint" and self.currentMoving.getTime() == 1360:  # we reached the end of forward.motion
                    self.currentMoving.setTime(360)  # loop back to the beginning of the walking sequence

                return self.motions.ForwardsSprint

        # The ball on right zone.
        else:
            # If the ball on team member.
            if self.knowBallOwner()[0] == "R" and self.knowBallOwner() != "RedDefender2" and self.knowBallOwner() != "RedGoalKeeper":

                # Go to zone 9.
                if RedTeamStrategy.getZone(selfCoordinate) != 9:
                    # print("I am going to 9")
                    # Bottom line of zone 9.
                    zoneTargetX = (RedTeamStrategy.PLAY_ZONE[9][0][0] + RedTeamStrategy.PLAY_ZONE[9][1][0]) / 2
                    zoneTargetY = RedTeamStrategy.PLAY_ZONE[9][0][1]
                    # Find the angle between the target zone and robot heading.
                    turningAngle = BasicFunction.calculateTurnAngle([zoneTargetX, zoneTargetY],
                                                                                          selfCoordinate,
                                                                                          robotHeadingAngle)
                    turningMotion = self.getTurnMotion(turningAngle)
                    if turningMotion is not None:
                        return turningMotion

                    # Check if there is an obstacle in front of the robot.
                    if self.obstacleAvoidance:
                        if leftDistance < 0.75:
                            return self.motions.SideStepRight
                        elif rightDistance < 0.75:
                            return self.motions.SideStepLeft

                    if self.currentMoving and self.currentMoving.name == "ForwardsSprint" and self.currentMoving.getTime() == 1360:  # we reached the end of forward.motion
                        self.currentMoving.setTime(360)  # loop back to the beginning of the walking sequence

                    return self.motions.ForwardsSprint

                # Head to ball.
                else:
                    # print("I am waiting on 9")
                    # Find the angle between the ball and robot heading.
                    turningAngle = BasicFunction.calculateTurnAngle(ballCoordinate,
                                                                                          selfCoordinate,
                                                                                          robotHeadingAngle)
                    turningMotion = self.getTurnMotion(turningAngle)
                    if turningMotion is not None:
                        return turningMotion

            # The ball on the opponent.
            else:
                # Go to zone 6.
                if RedTeamStrategy.getZone(selfCoordinate) != 6:
                    # print("I am going to 6")
                    # Bottom line of zone 6.
                    zoneTargetX = (RedTeamStrategy.PLAY_ZONE[6][0][0] + RedTeamStrategy.PLAY_ZONE[6][1][0]) / 2
                    zoneTargetY = RedTeamStrategy.PLAY_ZONE[6][0][1]
                    # Find the angle between the target zone and robot heading.
                    turningAngle = BasicFunction.calculateTurnAngle([zoneTargetX, zoneTargetY],
                                                                                          selfCoordinate,
                                                                                          robotHeadingAngle)
                    turningMotion = self.getTurnMotion(turningAngle)
                    if turningMotion is not None:
                        return turningMotion

                    # Check if there is an obstacle in front of the robot.
                    if self.obstacleAvoidance:
                        if leftDistance < 0.75:
                            return self.motions.SideStepRight
                        elif rightDistance < 0.75:
                            return self.motions.SideStepLeft

                    if self.currentMoving and self.currentMoving.name == "ForwardsSprint" and self.currentMoving.getTime() == 1360:  # we reached the end of forward.motion
                        self.currentMoving.setTime(360)  # loop back to the beginning of the walking sequence

                    return self.motions.ForwardsSprint

                # Head to ball.
                else:
                    # print("I am waiting on 6")
                    # Find the angle between the ball and robot heading.
                    turningAngle = BasicFunction.calculateTurnAngle(ballCoordinate,
                                                                                          selfCoordinate,
                                                                                          robotHeadingAngle)
                    turningMotion = self.getTurnMotion(turningAngle)
                    if turningMotion is not None:
                        return turningMotion

        # Stand by.
        return self.motions.StandInit