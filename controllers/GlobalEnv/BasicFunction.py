'''基础函数
1，计算距离
2，计算球的与X轴角度
3，计算球所在区域
4，计算转向角度
'''
import math
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(currentdir)
sys.path.append(parentdir)
#计算距离
def calculateDistance (coordinate1,coordinate2) ->float:
    """
    this function is calculate distance between coordinate1 and coordinate2
    :param coordinate1:
    :param coordinate2:
    :return:distance
    """
    deltX = math.fabs(coordinate1[0]-coordinate2[0])
    deltY = math.fabs(coordinate1[1]-coordinate2[1])
    return math.hypot(deltX,deltY)
def calculateBallAngleToX(ball_coordinate,robot_coordinate):

    hypot = calculateDistance(ball_coordinate,robot_coordinate)
    deltX = math.fabs(ball_coordinate[0]-robot_coordinate[0])
    cosTheta = deltX/hypot
    degree  = math.degrees(math.cos(cosTheta))
    return degree
def calculateBallRegionAccordingToRobot(ball_coordinate,robot_coordinate):
    """
    计算球相对于机器人的位置
    :param ball_coordinate:
    :param robot_coordinate:
    :return:
    """
    if ball_coordinate[0] > robot_coordinate[0]:
        if ball_coordinate[1]>robot_coordinate[1]:
            ballRagion = 1
        else:
            ballRagion = 4
    else:
        if ball_coordinate[1]>robot_coordinate[1]:
            ballRagion = 2
        else:
            ballRagion = 3
    return ballRagion

def calculateTurnAngle(ball_coordinate,robot_coordinate,robotHeadingAngle):
    degree = calculateBallAngleToX(ball_coordinate,robot_coordinate)
    ball_region = calculateBallRegionAccordingToRobot(ball_coordinate,robot_coordinate)

    if ball_region == 2:
        degree = 180 - degree
    elif ball_region ==3:
        degree = degree-180
    elif ball_region ==4:
        degree = -degree

    zDegree = math.degrees(robotHeadingAngle)
    turning_angle = degree - zDegree
    if turning_angle>180:
        turning_angle = turning_angle-360
    elif turning_angle <-180:
        turning_angle = turning_angle+360

    return turning_angle



