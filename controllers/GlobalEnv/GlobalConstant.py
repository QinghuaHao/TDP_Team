from controller import Motion
import math
from enum import Enum

#全局变量
TIME_STEP = 32 #enable devices
Pi = math.pi
#初始位置
Initial_Positions = {
  "BALL"      : [ 0.00,  0.00, 0.079875],
  "Red_Goalkeeper"    : [-4.00,  0.00, 0.334],
  "Red_Defender_1" : [-1.6,  1.50, 0.334],
  "Red_Defender_2" : [-1.6, -1.50, 0.334],
  "Red_Striker_1"    : [-1,  0.00, 0.334],
  "Blue_Goalkeeper"   : [ 4.00,  0.00, 0.334],
  "Blue_Defender_1"  : [1.6,  1.50, 0.334],
  "Blue_Defender_2"  : [1.6, -1.50, 0.334],
  "Blue_Striker_1"  : [ 1,  0, 0.334]
}

#禁区
ball_Position = {
  "OUT_R"     : [-3.65, 0, 0.0798759],
  "OUT_B"     : [ 3.65, 0, 0.0798759]
}

#初始转动
Initial_Rotations={
    "BALL": [0,1,0,0],
    "Red_Goalkeeper": [0,1,0,0],
    "Red_Defender_1": [0,1,0,0],
    "Red_Defender_2": [0,1,0,0],
    "Red_Striker_1": [0,1,0,0],
    "Blue_Goalkeeper": [0,0,1,-3.14159],
    "Blue_Defender_1": [0,1,0,-3.14159],
    "Blue_Defender_2": [0,1,0,-3.14159],
    "Blue_Striker_1": [0,1,0,-3.14159]
}
#球的位置


#loading motion file
class LoadMoveFile:
    def __init__(self):
        self.Backwards = MoveFileBase('Backwards','../../motions/Backwards.motion')
        self.Forwards = MoveFileBase('Forwards', '../../motions/Forwards.motion')
        self.Forwards50 = MoveFileBase('Forwards50', '../../motions/Forwards50.motion')
        self.ForwardsSprint = MoveFileBase('ForwardsSprint', '../../motions/ForwardsSprint.motion')
        self.HandWave = MoveFileBase('HandWave', '../../motions/HandWave.motion')
        self.LongPass = MoveFileBase('LongPass', '../../motions/LongPass.motion')
        self.RightShoot = MoveFileBase('RightShoot', '../../motions/RightShoot.motion')
        self.Shoot = MoveFileBase('Shoot', '../../motions/Shoot.motion')
        self.SidePass_Left = MoveFileBase('SidePass_Left', '../../motions/SidePass_Left.motion')
        self.SidePass_Right = MoveFileBase('SidePass_Right', '../../motions/SidePass_Right.motion')
        self.SideStepLeft = MoveFileBase('SideStepLeft', '../../motions/SideStepLeft.motion')
        self.SideStepRight = MoveFileBase('SideStepRight', '../../motions/SideStepRight.motion')
        self.StandInit = MoveFileBase('StandInit', '../../motions/StandInit.motion')
        self.StandUpFromBack = MoveFileBase('StandUpFromBack', '../../motions/StandUpFromBack.motion')
        self.StandUpFromFront = MoveFileBase('StandUpFromFront', '../../motions/StandUpFromFront.motion')
        self.TurnLeft10_V2 = MoveFileBase('TurnLeft10_V2', '../../motions/TurnLeft10_V2.motion')
        self.TurnLeft10 = MoveFileBase('TurnLeft10', '../../motions/TurnLeft10.motion')
        self.TurnLeft20 = MoveFileBase('TurnLeft20', '../../motions/TurnLeft20.motion')
        self.TurnLeft30 = MoveFileBase('TurnLeft30', '../../motions/TurnLeft30.motion')
        self.TurnLeft40 = MoveFileBase('TurnLeft40', '../../motions/TurnLeft40.motion')
        self.TurnLeft60 = MoveFileBase('TurnLeft60', '../../motions/TurnLeft60.motion')
        self.TurnLeft180 = MoveFileBase('TurnLeft180', '../../motions/TurnLeft180.motion')
        self.TurnRight10_V2 = MoveFileBase('TurnRight10_V2', '../../motions/TurnRight10_V2.motion')
        self.TurnRight10 = MoveFileBase('TurnRight10', '../../motions/TurnRight10.motion')
        self.TurnRight40 = MoveFileBase('TurnRight40', '../../motions/TurnRight40.motion')
        self.TurnRight60 = MoveFileBase('TurnRight60', '../../motions/TurnRight60.motion')

class MoveFileBase(LoadMoveFile):
    def __init__(self,name,path):
        super().__init__(path)
        self.name = name
