This is a simple python script to automate the mod staging process for OpenMW, an open source game engine. Maybe I'll do something more for it later, but that's later. It is tested and verified working as of OpenMW 0.46.

Before using, ensure that all mods in your mod staging folder are uncompressed, with the path "../MODNAME/Data Files" intact for each folder. 

Create a list of all mod staging folders in the file "modlist.cfg," to be placed in the same folder as ezmodstaging.py. 

The last line of 'modlist.cfg' must be the absolute path for the config file, 'openmw.cfg' 

The exact location depends on your operating system. Note that the config file is NOT the config file found in the OpenMW application folder. 

Once the config file has been modified, the original config file will be saved as "openmwOLD.cfg"

Default Config File locations: 
Linux: $HOME/.config/openmw 
Mac: $HOME/Library/Preferences/openmw
Windows: Documents\My Games\OpenMW