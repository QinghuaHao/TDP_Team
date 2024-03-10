import sys
sys.path.append('.')
sys.path.append('..')

from GlobalEnv.InitSupervisor import SupervisorBase
from GlobalEnv.GlobalConstant import TIME_STEP , LoadMoveFile
from ScoreBoard import Scoreboard
supervisor = SupervisorBase()
scoreboard = Scoreboard()

while supervisor.step(TIME_STEP)!=-1:
    scoreboard.updateScoreboard(supervisor)
    supervisor.sendsupervisorData()

