# Alten - PySc2 minigames

## Installation on Windows

The PySc2InstallPackage contains an install script (InstallPySc2.cmd), execute this script and follow the inscrutions.  
The script will:
 - Install Python
 - Install PySc2
 - Install Starcraft2

After the script finished copy the folder "Agents" to  
C:%homepath%\AppData\Local\Programs\Python\Python37-32\Lib\site-packages\pysc2

When you did this you can check if everything is installed successfully by running StartPySc2.cmd.  

## Installation on Linux

On Linux, you need Python, PySc2 and Starcraft2.

- Python can be installed with your favorite package manager.
- PySc2 can be installed with the instructions of [Deepmind](https://github.com/deepmind/pysc2).
- To install Starcraft2, you need to follow the instructions of [Blizzard](https://github.com/Blizzard/s2client-proto#downloads).

After installing, run the following commands:

```console
git clone https://github.com/AltenStarcraft/AltenStarcraft
cd AltenStarcraft
mkdir ~/StarCraftII/Maps/mini_games
cp ./Maps/MoveToBeacon.SC2Map ~/StarCraftII/Maps/mini_games/
```

This should set up your installation. After this, run the following command from `AltenStarcraft`:

```console
python -m pysc2.bin.agent --map MoveToBeacon --agent Agents.PySc2Agent.MoveToBeaconAgent
```

## Creating your own agent

The StartPySc2.cmd will basically set some variables to make it possible to start PySc2 and then start PySc2 by:  
%python% -m pysc2.bin.agent --map MoveToBeacon --agent pysc2.agents.PySc2Agent.MoveToBeaconAgent  

The map which will be started is defined by "--map ..."  
The agent which is started is defined by "--agent ..."  

The default map (mini game) which is started is the "move to beacon" map.


We already provided some python code which makes interacting with the PySc2 interface for the "move to beacon" map easier.  
We provided the following scripts:
- PySc2Agent.py -> this hides the agent initialisation
- MyAgent.py -> here you can create your own agent by changing the get_state, do_action and get_reward methods
- PySc2HelperFunctions.py -> these are helper functions to e.g. get the marine location, get the beacon location, create move to location action etc...
- MyAgent2.py -> this is an example sollution of the "move to beacon" map

As described in the "Installation" the "Agents" folder needs to be copied to C:%homepath%\AppData\Local\Programs\Python\Python37-32\Lib\site-packages\pysc2.  
Thus when working on your own SC2 agent you should be working in the C:%homepath%\AppData\Local\Programs\Python\Python37-32\Lib\site-packages\pysc2\Agents\MyAgents folder.  



## Future plans

More minigames with different AI techniques will follow!  
We are also thinking of creating some kind of competition.  


## More info on PySc2
https://github.com/deepmind/pysc2
