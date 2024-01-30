"""
守门员
1.丢球就找球
2.尽量和球保持在同一个Y轴坐标系上
3.球到门口，就面向禁区外任何一个队友方向踢
"""
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from GlobalConstant import TIME_STEP
import RedTeamStrategy
import BasicFunction
import InitRobot
class GoalKeeper(InitRobot.ScoreRobot):
    def run(self):
        while self.robot.step(TIME_STEP)!= -1:
            if self.isNewBallDataValuable():
                self.getsupervisorData()
                ballCoordinate = self.getBallData()
                selfCoordinate = self.getselfPostiton()
                decidedMotion = self.decidedMotion(ballCoordinate,selfCoordinate)
                if self.isNewMotionValuable(decidedMotion):
                    forwardSprintBreak = self.currentMoving and (self.currentMoving.name == self.motions.ForwardsSprint.name != self.motions.ForwardsSprint.name)
                    leftShootCheck = self.currentMoving and self.currentMoving.name == self.motions.RightShoot.name and self.currentMoving.isOver() and decidedMotion.name == self.motions.RightShoot.name
                self.clearMotionList()
                if leftShootCheck:
                    self.loadMotionToList(self.motions.Shoot)
                else:
                    self.loadMotionToList(decidedMotion)
            self.startMotion()
        else:
            pass
    def decidedMotion(self,ballCoordinate,selfCoordinate):
        if self.checkGetScore() ==1:
            return self.motions.HandWave
        elif self.checkGetScore() == -1:
            return self.motions.StandInit
        robotHeightFromGound = self.getselfPostiton()[2]
        if robotHeightFromGound <0.2:
            if self.getleftsonarDistance()==2.55 and self.getrightsonarDistance()==2.25:
                return self.motions.StandUpFromBack
            else:
                return self.motions.StandUpFromFront

        if self.checkBallpriority() =='B':
            return self.motions.StandInit
        robotHeadAngle = self.getRollPitchYaw()[2]

        if RedTeamStrategy.getZone(ballCoordinate) == 2:
            turn_angle = BasicFunction.calculateTurnAngle(ballCoordinate,selfCoordinate)
            turn_motion = self.getTurnMotion(turn_angle)
            if turn_motion is not None:
                return turn_motion
            body_distance_from_ball = BasicFunction.calculateDistance(ballCoordinate,selfCoordinate)
            if body_distance_from_ball <0.25:
                turn_angle_left = BasicFunction.calculateTurnAngle(RedTeamStrategy.RED_GOAL['Left'],selfCoordinate,robotHeadAngle)
                turn_angle_right = BasicFunction.calculateTurnAngle(RedTeamStrategy.RED_GOAL['Right'], selfCoordinate,robotHeadAngle)
                if (turn_angle_left>0 and turn_angle_right>0) or (turn_angle_left<0 and turn_angle_right<0) or\
                        ((abs(turn_angle_left)>90)and (abs(turn_angle_left)>abs(turn_angle_right))) or\
                        ((abs(turn_angle_left)>90 and (abs(turn_angle_left)<abs(turn_angle_right)))):
                    if body_distance_from_ball<0.2:
                        return self.motions.RightShoot
                    else:
                        return self.motions.ForwardsSprint
                else:
                    return self.motions.SideStepRight
            if self.currentMoving and self.currentMoving.name == 'ForwardsSprint' and self.currentMoving.getTime()==1360:
                self.currentMoving.setTime(360)
            return self.motions.ForwardsSprint
        else:
            turn_angle = BasicFunction.calculateTurnAngle(ballCoordinate,selfCoordinate,robotHeadAngle)
            turn_motion = self.getTurnMotion(turn_angle)
            if turn_motion is not None:
                return turn_motion
            return self.motions.StandInit



