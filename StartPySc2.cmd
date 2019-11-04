set Python=C:%homepath%\AppData\Local\Programs\Python\Python37-32\python
set Pip=C:%homepath%\AppData\Local\Programs\Python\Python37-32\Scripts\pip
set PySc2Root=C:%homepath%\AppData\Local\Programs\Python\Python37-32\Lib\site-packages\pysc2
set SC2PATH=C:\Program Files (x86)\StarCraft II
%python% -m pysc2.bin.agent --map MoveToBeacon --agent pysc2.agents.PySc2Agent.MoveToBeaconAgent

