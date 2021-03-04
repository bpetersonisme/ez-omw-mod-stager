from pathlib import Path 
import shutil
import sys
import tkinter as tk
import re

"""***************************************
                Methods
***************************************"""
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

#Returns a version of the target list without any entries it shares with blacklist 
def breakMatches(target, blacklist): 
    if (blacklist == [] or target == []):
        return (target)
    result = []
    for x in target: 
        if x not in blacklist: 
            result.append(x)
    return (result)

#Returns a version of the target list with only lines that match the specified regular expression  
def filterForLines(target, regex='[dD][aA][tT][aA] *= *".*"'): 
    result = [] 
    for cur in target:  
        hasMatch = re.match(regex, cur) 
        if(bool(hasMatch) == True):
            result.append(cur)  
    return result


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

def doProcess(self):  
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
    #Saves the original config file, if it does not exist already
    try: 
        confPath = Path(configLoc)
        oldConf = str(confPath.parent) + "\\openmwOLD"
        if(pathExists(oldConf + ".cfg") == False):
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
        #Reads the config file into a list 
        with open(configLoc) as origConfig: 
            configLines = origConfig.readlines()
        dataLines = filterForLines(configLines)
        for check in stagingFolderLocations:
            print (check)
        stagingFolderLocations = breakMatches(stagingFolderLocations, dataLines)
        

        
        #Puts the finished config file together 
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
        print("File not found!") 
    

"""********************************

    Classes

********************************"""
class modstage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        


"""********************************

    The main part of the program 
    
********************************"""

if __name__ == "__main__":
    #Sets up the GUI's execution loop, to run for the program lifetime 

    window_main = tk.Tk(className='OpenMW Mod Stager')
    window_main.geometry("400x200")

    frame_1 = tk.Frame(window_main, bg='#c4ffd2', width=200, height=50)

    app = modstage()
 

    app.mainloop()
    
    
 
