import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(currentdir)
sys.path.append(parentdir)

from controller import Motion,InertialUnit
from abc import ABC,abstractmethod
from GlobalConstant import TIME_STEP,LoadMoveFile
import struct
class ScoreRobot(ABC):
    #初始化硬件
    def __init__(self,robot):
        self.robot = robot
        self.name = robot.getName()

        self.supervisorDate = None

        #GPS
        self.gps = robot.getDevice("gps")
        self.gps.enable(TIME_STEP)

        #Receiver
        self.receiver = robot.getDevice('receiver')
        self.receiver.enable(TIME_STEP)

        #Emitter
        self.emitter = robot.getDevice('emitter')


        #inertial unit
        self.inertialunit = robot.getDevice('inertial unit')
        self.inertialunit.enable(TIME_STEP)

        #sound sensor
        self.soundsensor = []
        self.soundsensor.append(robot.getDevice("Sonar/Left"))
        self.soundsensor.append(robot.getDevice("Sonar/Right"))
        self.soundsensor[0].enable(TIME_STEP)
        self.soundsensor[1].enable(TIME_STEP)


        #Obstacle Avoidance Option
        self.obstacleAvoidance = True


        #Foot Bumpers
        self.bumpers = {
            'bumperLL':robot.getDevice('LFoot/Bumper/Left'),
            'bumperLR': robot.getDevice('LFoot/Bumper/Right'),
            'bumperRL': robot.getDevice('RFoot/Bumper/Left'),
            'bumperRR': robot.getDevice('RFoot/Bumper/Right')
        }
        self.bumpers['bumperLL'].enable(TIME_STEP)
        self.bumpers['bumperLR'].enable(TIME_STEP)
        self.bumpers['bumperRL'].enable(TIME_STEP)
        self.bumpers['bumperRR'].enable(TIME_STEP)

        #Camera
        self.cameraTop = robot.getDevice('CameraTop')
        self.cameraBottom = robot.getDevice('CameraBottom')
        self.cameraBottom.enable(TIME_STEP)
        self.cameraTop.enable(TIME_STEP)

        #Load motions file
        self.motions = LoadMoveFile()
        self.currentMoving = False
        self.motionsQueue = [self.motions.StandInit]
        self.startMotion()

    @abstractmethod
        #运动决定
    def decidedMotion(self,ballCoordinate,selfCoordinate):
        pass


        #打印自己
    def printSelf(self):
        print('hello world, this is robot named',self.name)


    #拿到自己坐标
    def getselfPostiton(self):
        gps_values = self.gps.getValues()
        return [gps_values[0],gps_values[1],gps_values[2]]


     #拿到机器人横摇/俯仰/偏航角
    def getRollPitchYaw(self):
        return self.inertialunit.getRollPitchYaw()


    #确定球
    def isNewBallDataValuable(self):
        return self.receiver.getData() >0


    #拿到观察者数据
    def getsupervisorData(self):
        message=self.receiver.getData()
        self.supervisorData = struct.unpack('dd9cc24d',message)
        self.receiver.nextPacket()


    #拿到球的数据
    def getBallData(self):
        return [self.supervisorData[0],self.supervisorData[1]]  #初始化supervisor中可以查看


    #拿到左面距离（sonar）
    def getleftsonarDistance(self):
        return self.soundsensor[0].getValues()


    #拿到右距离（sonar）
    def getrightsonarDistance(self):
        return self.soundsensor[1].getValues()

    #知道谁拿着球
    def knowBallOwner(self):
        ballowner = ''
        for i in range(2,11):
            ballowner = ballowner +self.supervisorData[i].decode('utf-8')
        return ballowner.strip('*')


    #球的优先级
    def checkBallpriority(self):
        return self.supervisorData[11].decode('utf-8')



    #检查是否进球
    def checkGetScore(self):
        ballCoordination = self.getBallData()
        if abs(ballCoordination[0])>4.5 and abs(ballCoordination[1])<1.35:
            if 4.5 < ballCoordination[0]:
                if self.name[0] == "R":
                    return 1
                else:
                    return -1

            else:
                if self.name[0] == "B":
                    return 1
                else:
                    return -1
        return 0

    #打断运动
    def breakMotion(self):
        if self.currentMoving:
            self.currentMoving.stop()
            self.currentMoving =False


    #打断向前冲刺
    def breakForwardMotion(self):
        if self.currentMoving and self.currentMoving.name == 'forwardsSprint' and self.currentMoving.getTime()==1360:
            self.currentMoving.stop()
            self.currentMoving =False


    #开始运动
    def startMotion(self):
        if self.currentMoving == False or self.currentMoving.isOver():
            if len(self.motionsQueue) > 0:
                currentMotion = self.motionsQueue.pop(0)
                currentMotion.play()
                self.currentMoving = currentMotion


    #加载运动到队列
    def loadMotionToList(self,motion):
        return self.motionsQueue.append(motion)


    #清除运动队列
    def clearMotionList(self):
        self.motionsQueue.clear()


    #判断新的运动是否有效
    def isNewMotionValuable(self,newMotion):

        if newMotion == None or (self.currentMoving != False and self.currentMoving.isOver() != True and newMotion.name == self.currentMoving.name):
            return False
        return True


    #拿到转向角度
    def getTurnMotion(self,turnangle):
        if turnangle >50:
            return self.motions.TurnLeft60
        elif turnangle > 20:
            return self.motions.TurnLeft30
        elif turnangle < -50:
            return self.motions.TurnRight60
        elif turnangle < -30:
            return self.motions.TurnRight40
        else:
            return None



