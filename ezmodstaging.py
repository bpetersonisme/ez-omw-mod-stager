from pathlib import Path 
import shutil
import sys

#This creates the mod data list, based off the directories in somePath
def printConfig(somePath): 
    rest = [] 
    try: 
        txt_folder = Path(somePath) 
        folderBetter = txt_folder.iterdir()
        for cur in folderBetter:
            if(cur.is_dir() == True):  
                rest.append("data=\"" + str(cur) + "\\Data Files\"\n")
    except FileNotFoundError: 
        pass
    return rest


#Returns true if the string input is a valid directory, and false otherwise
def isPath(somePath):
    possFolder = Path(somePath) 
    return (pathExists(somePath) and possFolder.is_dir()) 


#Returns true if the string input is the file path to the openmw config file 
def isConfig(somePath):
    possConfig = Path(somePath) 
    return (pathExists(somePath) == True and possConfig.name == "openmw.cfg")


#Returns true if the string input actually exists 
def pathExists(somePath):
    posPath = Path(somePath)
    result = False 
    try: 
        result = posPath.exists() 
    except OSError: 
        pass 
    return (result)




"""
    The main part of the program 
"""
modList = []
configLoc = ""

#This creates the config file if, for some reason, it doesn't exist yet 
try: 
    conFile = open('modlist.cfg', 'x') 
    conFile.close()
except FileExistsError:
    pass
    
#This part reads the mod staging folder and config list, if there is anything to read. 
try: 
    with open('modlist.cfg') as thisFile:     
        stageList = thisFile.readlines() 
        if (len (stageList) < 2):
            sys.exit('Either you have entered no config folder location, or you do not have any mod staging folders. Either way, there is nothing to be done by this program. Goodbye.')
        else:
            modList = stageList.copy() 
            configLoc = modList.pop()
except IOError:
    sys.exit("Do not have permission to perform this operation!")
#Checks to see if the path given to the config file is valid 
try: 
    if(isConfig(configLoc) == False):
        sys.exit("Fatal Error: Config file not found!")
except OSError: 
    sys.exit("Fatal Error: The path \"" + configLoc + "\" is not valid for your operating system")
    
try: 
    confPath = Path(configLoc)
    oldConf = str(confPath.parent) + "\\openmwOLD"
    if(pathExists(oldConf + ".cfg")):
        i = 1 
        while(pathExists(oldConf + " (" + str(i) + ").cfg")):
            i = i + 1
        oldConf = oldConf + " (" + str(i) + ").cfg"
    else:
        oldConf = oldConf + ".cfg"
    shutil.copy(configLoc, oldConf)
#    with open(configLoc, 'w') as omwConfig:        
except IOError: 
    sys.exit("IO Error!")


stagingFolderLocations = [] 
#This part creates an iterable list of all mod folders specified 
for raw in modList: 
    cur = raw[0:-1]  
    if (isPath(cur) == True):
        stagingFolderLocations = stagingFolderLocations + (printConfig(cur))

 

configLines = []

try:
    with open(configLoc) as origConfig: 
        configLines = origConfig.readlines()
    with open(configLoc, 'w') as configFile:
        inData = False 
        for cur in configLines:
            if("data=" not in cur):
                if(inData == True): 
                    for thisData in stagingFolderLocations: 
                        configFile.write(thisData) 
                        inData = False
                configFile.write(cur)
            else: 
                inData = True
                configFile.write(cur)
except IOError:
    sys.exit("IO Error!")
except FileNotFoundError: 
    print("File not found! Will move on to next.") 
"""
#This is the main part of the program 
modStagingFolder = ""
configPlace = ""
if(len(sys.argv) == 2 and (isPath(sys.argv[1]) == True)):
    modStagingFolder = sys.argv[1]
elif(len(sys.argv) == 3):
    if((isPath(sys.argv[1]) == True)):
        modStagingFolder = sys.argv[1]
    if(isConfig(sys.argv[2] == True)):
        configPlace = sys.argv[2]


#Accepts user input for the mod staging folder, if that is not already specified 
while (modStagingFolder == ""):
    modStagingFolder = input("Please enter your mod staging folder URI here. (No quotes needed)\n") 
    if (isPath(modStagingFolder) == False):
        if(modStagingFolder == "" or modStagingFolder.lower() == "no" or modStagingFolder.lower() == "quit" or modStagingFolder.lower() == "n"):
            sys.exit("Okay.")
        else:
            modStagingFolder = ""
            print("Invalid input!", end=" ") 
 
while (modStagingFolder == ""):
    modStagingFolder = input("Please enter your mod staging folder URI here. (No quotes needed)\n") 
    if (isPath(modStagingFolder) == False):
        if(modStagingFolder == "" or modStagingFolder.lower() == "no" or modStagingFolder.lower() == "quit" or modStagingFolder.lower() == "n"):
            sys.exit("Okay.")
        else:
            modStagingFolder = ""
            print("Invalid input!", end=" ") 
            
"""
 