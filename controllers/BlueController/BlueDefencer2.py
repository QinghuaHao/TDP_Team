"""
Blue Team Left Forward robot behaviours.
"""

import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from GlobalEnv.InitRobot import SoccerRobot
from GlobalEnv import BasicFunction
from GlobalEnv.GlobalConstant import (TIME_STEP, LoadMoveFile)


class ForwardRight(SoccerRobot):

    def run(self):
        self.printSelf()
        post_coordinate = [-4.86, 0.564, 0.0799]
        useless_flag = 0
        flag1 = 0
        flag2 = 0
        goto_Coordinate = [0, 0, 0]
        count_0 = 0
        while self.robot.step(TIME_STEP) != -1:

            if self.isNewBallDataValuable():
                self.getsupervisorData()
                # Use the ballData (location) to do something.
                data = self.supervisorData
                ballOwner = self.knowBallOwner()
                ballCoordinate = self.getBallData()
                selfCoordinate = self.getselfPostiton()
                leftForward = [data[30], data[31], data[32]]
                redForward = [data[21], data[22], data[23]]
                blueDef = [data[27], data[28], data[29]]

                # Check the goal scored to balance itself.
                if self.checkGetScore() == 1:
                    decidedMotion = self.motions.handWave

                    if self.isNewMotionValuable(decidedMotion):
                        boolean = self.currentMoving and \
                                  (self.currentMoving.name == self.motions.Forwards50.name and decidedMotion.name != self.motions.Forwards50.name)
                        if boolean:
                            self.breakMotion()
                        self.clearMotionList()
                        if boolean:
                            self.loadMotionToList(self.motions.StandInit)
                        self.loadMotionToList(decidedMotion)

                    self.startMotion()

                elif self.checkGetScore() == -1:
                    decidedMotion = self.motions.StandInit

                    if self.isNewMotionValuable(decidedMotion):
                        boolean = self.currentMoving and \
                                  (self.currentMoving.name == self.motions.Forwards50.name and decidedMotion.name != self.motions.Forwards50.name)
                        if boolean:
                            self.breakMotion()
                        self.clearMotionList()
                        if boolean:
                            self.loadMotionToList(self.motions.StandInit)
                        self.loadMotionToList(decidedMotion)

                    self.startMotion()

                # Check whether the robot falls down.
                robotHeightFromGround = selfCoordinate[2]

                if robotHeightFromGround < 0.2:
                    if self.getleftsonarDistance() == 2.55 and self.getrightsonarDistance() == 2.55:
                        decidedMotion = self.motions.StandUpFromBack
                    else:
                        decidedMotion = self.motions.StandUpFromFront

                    if self.isNewMotionValuable(decidedMotion):
                        boolean = self.currentMoving and \
                                  ( self.currentMoving.name == self.motions.Forwards50.name and decidedMotion.name != self.motions.Forwards50.name)
                        if boolean:
                            self.breakMotion()
                        self.clearMotionList()
                        if boolean:
                            self.loadMotionToList(self.motions.StandInit)
                        self.loadMotionToList(decidedMotion)

                    self.startMotion()

                # Check the oponent has ball priority.
                elif self.checkBallpriority() == "R":
                    decidedMotion = self.motions.StandInit

                    if self.isNewMotionValuable(decidedMotion):
                        boolean = self.currentMoving and \
                                  (
                                              self.currentMoving.name == self.motions.Forwards50.name and decidedMotion.name != self.motions.Forwards50.name)
                        if boolean:
                            self.breakMotion()
                        self.clearMotionList()
                        if boolean:
                            self.loadMotionToList(self.motions.StandInit)
                        self.loadMotionToList(decidedMotion)

                    self.startMotion()

                else:
                    if flag1 == 0:
                        if ballOwner == 'BlueDefencer2' or ballOwner[0] == 'R':
                            decidedMotion, flag1 = self.decidedMotion(ballCoordinate, selfCoordinate, post_coordinate)
                            if self.isNewMotionValuable(decidedMotion):
                                boolean = self.currentMoving and \
                                          (self.currentMoving.name == self.motions.Forwards50.name and decidedMotion.name != self.motions.Forwards50.name)
                                if boolean:
                                    self.breakMotion()
                                self.currentMoving()
                                if boolean:
                                    self.loadMotionToList(self.motions.StandInit)
                                self.loadMotionToList(decidedMotion)

                            self.startMotion()
                        elif ballOwner == ('BlueDefencer1'):
                            if leftForward[0] > -4.47 and leftForward[0] < 4.44 and leftForward[1] < 0 and leftForward[
                                1] > -1.5:
                                goto_Coordinate[0] = leftForward[0] - 1.5
                                goto_Coordinate[1] = leftForward[0] + 1.67
                                goto_Coordinate[2] = 0.343
                                decidedMotion, useless_flag = self.decidedMotion(goto_Coordinate, selfCoordinate,
                                                                                post_coordinate)
                                if self.isNewMotionValuable(decidedMotion):
                                    boolean = self.currentMoving and \
                                              (
                                                          self.currentMoving.name == self.motions.Forwards50.name and decidedMotion.name != self.motions.Forwards50.name)
                                    if boolean:
                                        self.breakMotion()
                                    self.clearMotionList()
                                    if boolean:
                                        self.loadMotionToList(self.motions.StandInit)
                                    self.loadMotionToList(decidedMotion)

                                self.startMotion()

                            elif leftForward[0] > -4.47 and leftForward[0] <= 0.268 and leftForward[1] < -1.5 and \
                                    leftForward[1] > -2.96:
                                goto_Coordinate[0] = leftForward[0] + 1.5
                                goto_Coordinate[1] = leftForward[0] + 1
                                goto_Coordinate[2] = 0.343
                                decidedMotion, useless_flag = self.decidedMotion(goto_Coordinate, selfCoordinate,
                                                                                post_coordinate)
                                if self.isNewMotionValuable(decidedMotion):
                                    boolean = self.currentMoving and \
                                              (
                                                          self.currentMoving.name == self.motions.Forwards50.name and decidedMotion.name != self.motions.Forwards50.name)
                                    if boolean:
                                        self.breakMotion()
                                    self.clearMotionList()
                                    if boolean:
                                        self.loadMotionToList(self.motions.StandInit)
                                    self.loadMotionToList(decidedMotion)

                                self.startMotion()

                            else:
                                goto_Coordinate[0] = leftForward[0] - 1
                                goto_Coordinate[1] = leftForward[0] + 1
                                goto_Coordinate[2] = 0.343
                                decidedMotion, useless_flag = self.decidedMotion(goto_Coordinate, selfCoordinate,
                                                                                post_coordinate)
                                if self.isNewMotionValuable(decidedMotion):
                                    boolean = self.currentMoving and \
                                              (self.currentMoving.name == self.motions.Forwards50.name and decidedMotion.name != self.motions.Forwards50.name)
                                    if boolean:
                                        self.breakMotion()
                                    self.clearMotionList()
                                    if boolean:
                                        self.loadMotionToList(self.motions.StandInit)
                                    self.loadMotionToList(decidedMotion)

                                self.startMotion()

                        elif (ballOwner == 'BLUE_DEF' or ballOwner == 'BLUE_GK'):
                            if ballCoordinate[0] <= 2.52 or (ballCoordinate[1] >= 2.4 and ballCoordinate[1] <= 2.98):
                                decidedMotion, flag1 = self.decidedMotion(ballCoordinate, selfCoordinate,
                                                                         post_coordinate)
                                if self.isNewMotionValuable(decidedMotion):
                                    boolean = self.currentMoving and \
                                              (
                                                          self.currentMoving.name == self.motions.forwards50.name and decidedMotion.name != self.motions.forwards50.name)
                                    if boolean:
                                        self.breakMotion()
                                    self.clearMotionList()
                                    if boolean:
                                        self.loadMotionToList(self.motions.StandInit)
                                    self.loadMotionToList(decidedMotion)

                                self.startMotion()

                            elif redForward[0] > 2.51 and redForward[1] >= 0 and redForward[1] <= 2.5:
                                goto_Coordinate[0] = 3.77
                                goto_Coordinate[1] = -0.698
                                goto_Coordinate[2] = 0.315
                                decidedMotion, useless_flag = self.decidedMotion(goto_Coordinate, selfCoordinate,
                                                                                post_coordinate)
                                if self.isNewMotionValuable(decidedMotion):
                                    boolean = self.currentMoving and \
                                              (
                                                          self.currentMoving.name == self.motions.forwards50.name and decidedMotion.name != self.motions.forwards50.name)
                                    if boolean:
                                        self.breakMotion()
                                    self.clearMotionList()
                                    if boolean:
                                        self.loadMotionToList(self.motions.StandInit)
                                    self.loadMotionToList(decidedMotion)

                                self.startMotion()

                            else:
                                decidedMotion = self.turnMotion(blueDef, selfCoordinate)
                                if self.isNewMotionValuable(decidedMotion):
                                    boolean = self.currentMoving and \
                                              (
                                                          self.currentMoving.name == self.motions.forwards50.name and decidedMotion.name != self.motions.forwards50.name)
                                    if boolean:
                                        self.breakMotion()
                                    self.clearMotionList()
                                    if boolean:
                                        self.loadMotionToList(self.motions.StandInit)
                                    self.loadMotionToList(decidedMotion)

                                self.startMotion()


                    else:
                        decidedMotion, flag1 = self.turn_to_goal_post(post_coordinate, selfCoordinate, leftForward,
                                                                      redForward)
                        if count_0 >= 2:
                            decidedMotion = self.motions.rightShoot
                            count_0 = 0
                        if decidedMotion == self.motions.longShoot:
                            count_0 = count_0 + 1

                        if self.isNewMotionValuable(decidedMotion):
                            boolean = self.currentMoving and \
                                      (
                                                  self.currentMoving.name == self.motions.forwards50.name and decidedMotion.name != self.motions.forwards50.name)
                            if boolean:
                                self.breakMotion()
                            self.clearMotionList()
                            if boolean:
                                self.loadMotionToList(self.motions.StandInit)
                            self.loadMotionToList(decidedMotion)

                            # self.addMotionToQueue(decidedMotion)

                        self.startMotion()

            else:
                # It seems there is a problem.
                print("NO BALL DATA!!!")

    # Override decidedMotion
    def decidedMotion(self, ballCoordinate, selfCoordinate, post_coordinate):

        robotHeadingAngle = self.getRollPitchYaw()[2]
        distanceFromBall = BasicFunction.calculateDistance(ballCoordinate, selfCoordinate)

        if distanceFromBall < 0.22:
            return self.motions.HandWave, 1
        turningAngle = BasicFunction.calculateDistance(ballCoordinate, selfCoordinate,
                                                                              robotHeadingAngle)

        if turningAngle > 50:
            return self.motions.TurnLeft60, 0
        elif turningAngle > 30:
            return self.motions.TurnLeft40, 0
        # elif turningAngle >= 10:
        #   return self.motions.turnLeft10,0
        elif turningAngle < -50:
            return self.motions.TurnRight60, 0
        elif turningAngle < -30:
            return self.motions.TurnRight40, 0
        # elif turningAngle < -20:
        #   return self.motions.turnRight10,0

        return self.motions.Forwards50, 0

    def turn_to_goal_post(self, post_coordinate, selfCoordinate, leftForward, redForward):

        self.clearMotionList()
        robotHeadingAngle = self.getRollPitchYaw()[2]
        turningAngle = BasicFunction.calculateTurnAngle(post_coordinate, selfCoordinate,
                                                                              robotHeadingAngle)
        if ((redForward[0] >= (selfCoordinate[0] - 0.5) and redForward[0] < selfCoordinate[0]) or (
                redForward[1] >= (selfCoordinate[1] - 0.45) and redForward[1] < selfCoordinate[1]) or (
                redForward[0] <= (selfCoordinate[0] + 0.5) and redForward[0] > selfCoordinate[0]) or (
                redForward[1] <= (selfCoordinate[1] + 0.45) and redForward[1] > selfCoordinate[1])):
            return self.pass_to_left(selfCoordinate, leftForward)

        else:
            if turningAngle > 90:
                return self.motions.SidePass_Right, 0
            elif turningAngle > 50:
                return self.motions.SidePass_Right, 0
            elif turningAngle > 30:
                return self.motions.SidePass_Right, 0
            elif turningAngle < -50:
                return self.motions.SidePass_Left, 0
            elif turningAngle < -30:
                return self.motions.SidePass_Left, 0
            else:
                return self.motions.Shoot, 0

    def check_position(self, selfCoordinate, leftForward):

        if (leftForward[0] <= (selfCoordinate[0]) and leftForward[1] > selfCoordinate[1]):
            return True
        else:
            return False

    def pass_to_left(self, selfCoordinate, leftForward):
        robotHeadingAngle = self.getRollPitchYaw()[2]
        turningAngle = BasicFunction.calculateTurnAngle(leftForward, selfCoordinate,
                                                                              robotHeadingAngle)
        if turningAngle > 90:
            return self.motions.SidePass_Right, 0
        elif turningAngle > 50:
            return self.motions.SidePass_Right, 0
        elif turningAngle > 30:
            return self.motions.Shoot, 0
        elif turningAngle < -50:
            return self.motions.SidePass_Right, 0
        elif turningAngle < -30:
            return self.motions.Shoot, 0
        else:
            return self.motions.Shoot, 0

    def turnMotion(self, ballCoordinate, selfCoordinate):
        robotHeadingAngle = self.getRollPitchYaw()[2]
        turningAngle = BasicFunction.calculateTurnAngle(ballCoordinate, selfCoordinate,
                                                                              robotHeadingAngle)

        if turningAngle > 90:
            return self.motions.TurnLeft180
        elif turningAngle > 50:
            return self.motions.TurnLeft60
        elif turningAngle > 30:
            return self.motions.TurnLeft40
        elif turningAngle < -50:
            return self.motions.TurnRight60
        elif turningAngle < -30:
            return self.motions.TurnRight40

        return self.motions.StandInit
        pass
