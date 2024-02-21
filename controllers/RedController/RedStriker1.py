"""
1，丢球就找球
2，球在地方半场，判断是否远
如果远，就传球
如果很近，就面向球门射门
"""
import sys
sys.path.append(".")
sys.path.append("..")
from GlobalEnv.InitRobot import SoccerRobot
from GlobalEnv.GlobalConstant import TIME_STEP,LoadMoveFile
from GlobalEnv import BasicFunction
import RedTeamStrategy


class Forward(SoccerRobot):
    def run(self):
        self.printSelf()
        while self.robot.step(TIME_STEP) != -1:

            if self.isNewBallDataValuable():


                # Do not remove this!
                # ----------------------
                self.getsupervisorData()
                # ----------------------

                # Use the ballData (location) to do something.
                ballCoordinate =self.getBallData()
                # print("RedForward - ballCoordinate: ", ballCoordinate)
                selfCoordinate = self.getselfPostiton()
                # print("RedForward - selfCoordinate: ", selfCoordinate)
                decidedMotion = self.decidedMotion(ballCoordinate, selfCoordinate)
                # print("RedForward - decidedMotion: ", decidedMotion.Name)
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
                    # print("RedForward - Motion interrupted!")
                    self.clearMotionList()
                    # if interruptCheck:
                    #   self.addMotionToQueue(self.motions.standInit)
                    if leftShootCheck:
                        self.loadMotionToList(self.motions.Shoot)
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
            return self.motions.handWave
        elif self.checkGetScore() == -1:
            return self.motions.standInit

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

            # The ball on team member.
            if self.knowBallOwner()[0] == "R" and self.knowBallOwner() != "RedStriker1":

                # Go to zone 14.
                if RedTeamStrategy.getZone(selfCoordinate) != 14:
                    # print("I am going to 14")
                    # Center of zone 14.
                    zoneCenterX = (RedTeamStrategy.PLAY_ZONE[14][0][0] + RedTeamStrategy.PLAY_ZONE[14][1][0]) / 2
                    zoneCenterY = (RedTeamStrategy.PLAY_ZONE[14][0][1] + RedTeamStrategy.PLAY_ZONE[14][1][1]) / 2
                    # Find the angle between the target zone and robot heading.
                    turningAngle = BasicFunction.calculateTurnAngle([zoneCenterX, zoneCenterY],
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
                    # print("I am waiting on 14")
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

                if self.currentMoving and self.currentMoving.name == "ForwardsSprint" and self.currentMoving.getTime() == 1360:  # we reached the end of forward.motion
                    self.currentMoving.setTime(360)  # loop back to the beginning of the walking sequence

                return self.motions.ForwardsSprint

        # The ball on team field.
        else:

            # It doesn't matter if the ball on opposite or team member.
            # Go to zone 11.
            if RedTeamStrategy.getZone(selfCoordinate) != 11:
                # print("I am going to 11")
                # Center of zone 11.
                zoneCenterX = (RedTeamStrategy.PLAY_ZONE[11][0][0] + RedTeamStrategy.PLAY_ZONE[11][1][0]) / 2
                zoneCenterY = (RedTeamStrategy.PLAY_ZONE[11][0][1] + RedTeamStrategy.PLAY_ZONE[11][1][1]) / 2
                # Find the angle between the target zone and robot heading.
                turningAngle = BasicFunction.calculateTurnAngle([zoneCenterX, zoneCenterY],
                                                                                      selfCoordinate, robotHeadingAngle)
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
                # print("I am waiting on 11")
                # Find the angle between the ball and robot heading.
                turningAngle = BasicFunction.calculateTurnAngle(ballCoordinate, selfCoordinate,
                                                                                      robotHeadingAngle)
                turningMotion = self.getTurnMotion(turningAngle)
                if turningMotion is not None:
                    return turningMotion

        # Stand by.
        return self.motions.StandInit