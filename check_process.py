import os
import time
import psutil
import configparser
import urllib.request

config = configparser.ConfigParser()
config_path = '%s\\.guufilesync\\' %  os.environ['LOCALAPPDATA']

def findProcessIdByName(processName):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    '''
    listOfProcessObjects = []
    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if processName.lower() in pinfo['name'].lower() :
               listOfProcessObjects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass
    return listOfProcessObjects

def check_if_game_is_running(process: str):
    listOfProcessIds = findProcessIdByName(process)
    if len(listOfProcessIds) > 0:
        for elem in listOfProcessIds:
            processName = elem['name']
            processCreationTime =  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(elem['create_time']))
            # print(processName, processCreationTime)
        return True
    else :
       return False

def check_for_new_save():
    config.read(f'{config_path}\\config.ini')
    link = "https://dl.gudx.dev/Grounded/saves/latest.zip"
    lastuser = "https://dl.gudx.dev/Grounded/.control/last_user.txt"
    f = urllib.request.urlopen(link)
    user = urllib.request.urlopen(lastuser)
    last_user_in_stack = None
    for line in user:
        last_user_in_stack = line.decode("utf-8")
    last_modified = f.headers['last-modified']
    if last_modified != config['TRACKER']['last_save'] and last_user_in_stack != config['SYSTEM']['user_name'] and config['SYSTEM']['save_folder'] != '(ID-GAMENUMBER)(LOGOUT-SAVE)':
        config['TRACKER']['last_save'] = last_modified
        config['TRACKER']['last_user'] = last_user_in_stack
        with open(f'{config_path}\\config.ini', 'w') as configfile:
                config.write(configfile)
        return True
    else:
        return False
    
def check_for_new_version():
    config.read(f'{config_path}\\config.ini')
    link = "https://dl.gudx.dev/Grounded/.control/version.guu"
    version_control = urllib.request.urlopen(link)
    version_master = None
    for line in version_control:
        version_master = line.decode("utf-8")
    if config['TRACKER']['version'] < version_master:
        return True
    return False