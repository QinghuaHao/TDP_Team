from controller import Supervisor
import struct
from GlobalConstant import TIME_STEP
import BasicFunction

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(currentdir)
sys.path.append(parentdir)
class SupervisorBase(Supervisor):
    def __init__(self):
        self.emitter = self.getDevice('emitter')
        self.ball = self.getFromDef('Ball')
        self.robots = {
            "Red_Goalkeeper": self.getFromDef('Red_Goalkeeper'),
            "Red_Striker_1" : self.getFromDef('Red_Striker_1'),
            "Red_Defender_1" : self.getFromDef('Red_Defender_1'),
            "Red_Defender_2": self.getFromDef('Red_Defender_2'),
            "Blue_Goalkeeper": self.getFromDef('Blue_Goalkeeper'),
            "Blue_Striker_1": self.getFromDef('Blue_Striker_1'),
            "Blue_Defender_2": self.getFromDef('Blue_Defender_2'),
            "Blue_Defender_1": self.getFromDef('Blue_Defender_1')
        }

        self.priority = "R"

        self.firstBallLocation = [0,0,0.079875]

        #拿到球的位置
    def getballPosition(self):
        ballTranslation = self.ball.getField('translation')
        newballLocation = ballTranslation.getSFVec3f()
        if abs(ballTranslation[0])<4.5 and abs(ballTranslation[1])<3:
            if (self.firstBallLocation[0] + 0.05 < self.firstBallLocation[0] or self.firstBallLocation[0] - 0.05 >
                    self.firstBallLocation[0] or \
                    self.firstBallLocation[1] + 0.05 < self.firstBallLocation[1] or self.firstBallLocation[1] - 0.05 >
                    self.firstBallLocation[1]):
                self.ballPriority = "N"
                self.previousBallLocation = newballLocation
        return newballLocation

        #设置球的位置
    def setballPosition(self,ballPosition):
        pass
        self.previousBallLocation = ballPosition
        ballTranslation = self.ball.getField("translation")
        ballTranslation.setSFVec3f(ballPosition)
        self.ball.resetPhysics()

        #拿到机器人坐标位置
    def getrobotPosition(self,robotName):
        robotTranslation = self.robots[robotName].getField("translation")
        return robotTranslation
        #得到拿球人

    def getballOwner(self):
        ballPosition = self.getrobotPosition()
        ballOwnerRobotName = ""
        minDistance = BasicFunction.calculateDistance(ballPosition,self.getrobotPosition(ballOwnerRobotName))
        for i, key in enumerate(self.robots):
            tempDistance = BasicFunction.calculateDistance(ballPosition,self.getrobotPosition(key))
            if tempDistance < minDistance:
                minDistance = tempDistance
                ballPosition= key
        if len(ballOwnerRobotName)<9:
            for i in range(len(ballOwnerRobotName),9):
                ballOwnerRobotName = ballOwnerRobotName + "*"
        return ballOwnerRobotName


        #向supervisor发送数据
    def sendsupervisorData(self):
        ballPosition = self.getballPosition()
        ballOwner = bytes(self.getballOwner(),'utf-8')
        ballPriority = bytes(self.ballPriority,'utf-8')
        """
          "BALL"      : [ 0.00,  0.00, 0.079875],
          "Red_Goalkeeper"    : [-4.00,  0.00, 0.334],
          "Red_Defender_1" : [-1.6,  1.50, 0.334],
          "Red_Defender_2" : [-1.6, -1.50, 0.334],
          "Red_Striker_1"    : [-1,  0.00, 0.334],
          "Blue_Goalkeeper"   : [ 4.00,  0.00, 0.334],
          "Blue_Defender_1"  : [1.6,  1.50, 0.334],
          "Blue_Defender_2"  : [1.6, -1.50, 0.334],
          "Blue_Striker_1"  : [ 1,  0, 0.334]
        """
        Red_Goalkeeper = self.getrobotPosition("Red_Goalkeeper")
        Red_Defender_1 = self.getrobotPosition("Red_Defender_1")
        Red_Defender_2 = self.getrobotPosition("Red_Defender_2")
        Red_Striker_1 = self.getrobotPosition("Red_Striker_1")
        Blue_Goalkeeper = self.getrobotPosition("Blue_Goalkeeper")
        Blue_Defender_1 = self.getrobotPosition("Blue_Defender_1")
        Blue_Defender_2 = self.getrobotPosition("Blue_Defender_2")
        Blue_Striker_1 = self.getrobotPosition("Blue_Striker_1")

        data = struct.pack('dd9ss24d',ballPosition[0],ballPosition[1],ballOwner,ballPriority,Red_Goalkeeper[0],Red_Goalkeeper[1],Red_Striker_1[0],Red_Striker_1[1],
                           Red_Defender_1[0],Red_Defender_1[1],Red_Defender_2[0],Red_Defender_2[1],Blue_Goalkeeper[0],Blue_Goalkeeper[1],
                           Blue_Striker_1[0],Blue_Striker_1[1],Blue_Defender_1[0],Blue_Defender_1[1],Blue_Defender_2[0],Blue_Defender_2[1])
        self.emitter.send(data)
        #设置球的优先级
    def setballPriority(self,priority):
        pass
        self.ballpriority = priority

        #重新开始模拟
    def restartSimulation(self):
        self.previousBallLocation =  [0,0,0.079875]
        self.restartSimulation()
        for robot in self.robots.values():
            robot.resetPhysics()

        #停止模拟
    def stopSimulation(self):
        self.simulationSetMode(self.SIMULATION_MODE_PAUSE)
