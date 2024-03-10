"""
Blue Team Defender robot behaviours.
"""

from SoccerRobotBase import SoccerRobot
import Functions
from Consts import (TIME_STEP,LoxadMoveFile)
from controller import Supervisor

class Defender(SoccerRobot):
    def run(self):
        self.printSelf()
        count_0 = 0
        flag = 0
        flag1 = 0
        fixedCoordinate = [3.1, -0.00573, 0.342]
        origin = [0.0723, -0.0798, 0.0799]
        goto_Coordinate = [0, 0, 0]
        while self.robot.step(TIME_STEP) != -1:

            if self.isNewBallDataValuable():
                self.getsupervisorData()
                # Use the ballData (location) to do something.
                data = self.supervisorData
                ballOwner = self.knowBallOwner()
                ballCoordinate = self.getBallData()
                blue_fw_l = [data[30], data[31], data[32]]
                blue_fw_r = [data[33], data[34], data[35]]
                redFw = [data[21], data[22], data[23]]
                # Get self coordinates
                selfCoordinate = self.getselfPostiton()

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
                elif self.checkBallpriority() == -1:
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
                        decidedMotion = self.motions.standUpFromBack
                    else:
                        decidedMotion = self.motions.standUpFromFront

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

                # Approach the ball only in penalty area
                else:
                    if ballCoordinate[0] >= 2.54 and ballCoordinate[0] <= 4.44:
                        flag = 1
                        if ballCoordinate[1] >= -1.5 and ballCoordinate[1] <= 1.5 and (
                                ballOwner == 'BLUE_GK' or ballOwner[0] == 'R'):
                            print('going to designated coordinates')
                            goto_Coordinate[0] = 4.22
                            goto_Coordinate[1] = -0.22
                            goto_Coordinate[2] = 0.315
                            decidedMotion = self.decidedMotion(ballCoordinate, selfCoordinate, blue_fw_l, blue_fw_r,
                                                              redFw)  # print("RedForward - decidedMotion: ", decidedMotion.Name)

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
                            decidedMotion = self.decidedMotion(ballCoordinate, selfCoordinate, blue_fw_l, blue_fw_r,
                                                              redFw)
                            if count_0 >= 2:
                                decidedMotion = self.motions.RightShoot
                                count_0 = 0
                            if decidedMotion == self.motions.LongPass:
                                count_0 = count_0 + 1

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
                        if (ballCoordinate[0] <= 2.54 or ballCoordinate[0] >= 4.44) and flag == 1:
                            flag1 = 0
                            decidedMotion = self.returnMotion(fixedCoordinate, selfCoordinate)
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
                            if (selfCoordinate[0] >= 2.8 and selfCoordinate[0] <= 3.2) and (
                                    selfCoordinate[1] >= -0.03 and selfCoordinate[1] <= 0):
                                flag = 0
                                flag1 = 1

                        if flag1 == 1:
                            decidedMotion = self.turnMotion(origin, selfCoordinate)
                            if self.isNewMotionValuable(decidedMotion):
                                boolean = self.currentMoving and \
                                          (
                                                      self.currentMoving.name == self.motions.Forwards50.name and decidedMotion.name != self.motions.Forwards50.name)
                                if boolean:
                                    self.isNewMotionValuable()
                                self.clearMotionList()
                                if boolean:
                                    self.loadMotionToList(self.motions.StandInit)
                                self.loadMotionToList(decidedMotion)

                            self.startMotion()

            else:

                print("NO BALL DATA!!!")

    def decidedMotion(self, ballCoordinate, selfCoordinate, blue_fw_l, blue_fw_r, redFw):
        robotHeadingAngle = self.getRollPitchYaw()[2]
        turningAngle = BasicFunction.calculateTurnAngle(ballCoordinate, selfCoordinate,
                                                                              robotHeadingAngle)

        if turningAngle > 50:
            return self.motions.TurnLeft60
        elif turningAngle > 30:
            return self.motions.TurnLeft40
        elif turningAngle < -50:
            return self.motions.TurnRight60
        elif turningAngle < -30:
            return self.motions.TurnRight40

        distanceFromBall = BasicFunction.calculateDistance(ballCoordinate, selfCoordinate)

        if distanceFromBall < 0.22:
            return self.passBall(selfCoordinate, blue_fw_l, blue_fw_r, redFw)

        return self.motions.Forwards50
        pass

    def returnMotion(self, ballCoordinate, selfCoordinate):
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

        return self.motions.Forwards50
        pass

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

    def passBall(self, selfCoordinate, blue_fw_l, blue_fw_r, redFw):
        if ((redFw[0] >= (blue_fw_l[0] - 0.5) and redFw[0] < blue_fw_l[0]) or (
                redFw[1] >= (blue_fw_l[1] - 0.45) and redFw[1] < blue_fw_l[1]) or (
                redFw[0] <= (blue_fw_l[0] + 0.5) and redFw[0] > blue_fw_l[0]) or (
                redFw[1] <= (blue_fw_l[1] + 0.45) and redFw[1] > blue_fw_l[1])):
            return self.pass_to_right(selfCoordinate, blue_fw_r)
        else:
            return self.pass_to_left(selfCoordinate, blue_fw_l)

        return self.pass_to_left(selfCoordinate, blue_fw_l)

    def pass_to_right(self, selfCoordinate, rightForward):
        robotHeadingAngle = self.getRollPitchYaw()[2]
        turningAngle = BasicFunction.calculateTurnAngle(rightForward, selfCoordinate,
                                                                              robotHeadingAngle)
        if turningAngle > 90:
            return self.motions.SidePass_Right
        elif turningAngle > 50:
            return self.motions.SidePass_Right
        elif turningAngle > 30:
            return self.motions.SidePass_Right
        elif turningAngle < -50:
            return self.motions.SidePass_Left
        elif turningAngle < -30:
            return self.motions.SidePass_Left
        else:
            return self.motions.Shoot

    def pass_to_left(self, selfCoordinate, leftForward):
        robotHeadingAngle = self.getRollPitchYaw()[2]
        turningAngle = BasicFunction.calculateTurnAngle(leftForward, selfCoordinate,
                                                                              robotHeadingAngle)
        if turningAngle > 90:
            return self.motions.SidePass_Right
        elif turningAngle > 50:
            return self.motions.SidePass_Right
        elif turningAngle > 30:
            return self.motions.SidePass_Right
        elif turningAngle < -50:
            return self.motions.SidePass_Left
        elif turningAngle < -30:
            return self.motions.SidePass_Left
        else:
            return self.motions.Shoot