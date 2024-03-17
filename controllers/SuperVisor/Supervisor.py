import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from Base.SupervisorBase import SupervisorBase
from Utils.Consts import (TIME_STEP, Motions)
from Scoreboard import Scoreboard

supervisor = SupervisorBase()
scoreboard = Scoreboard()

while supervisor.step(TIME_STEP) != -1:
    # The following code must be run to send the ball data to robots via emitter.
    print("Robot RED_FW: ", supervisor.getRobotPosition("RED_FW"))
    scoreboard.updateTimer(supervisor)
    scoreboard.updateScoreboard(supervisor)
    supervisor.setLabel(0, f"{scoreboard.timeRemainMinutes}:{scoreboard.timeRemain_s}", 0.07, 0, 0.4, 0xffff00, 0.1, "Times New Roman")
    supervisor.setLabel(1, "Red:Blue", 0.27, 0, 0.4, 0xffff00, 0.1,"Times New Roman")
    supervisor.setLabel(2, f"{scoreboard.redTeamScore}:{scoreboard.blueTeamScore}", 0.63, 0, 0.4, 0xffff00, 0.1,"Times New Roman")
    supervisor.sendSupervisorData()
    # print("Supervisor: ", supervisor.getBallPosition())
