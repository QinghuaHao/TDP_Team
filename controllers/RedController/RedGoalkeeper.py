"""
守门员
1.丢球就找球
2.尽量和球保持在同一个Y轴坐标系上
3.球到门口，就面向禁区外任何一个队友方向踢
"""
from InitRobot import ScoreRobot
from GlobalConstant import TIME_STEP
class GoalKeeper(ScoreRobot):
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

