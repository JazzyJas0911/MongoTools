#TODO

import os
import stat
import sys
import subprocess
import pymongo
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def dirinfo(fullpath):
    if("--verbose" in sys.argv):
        print("scanning " + fullpath)
    result=os.stat(fullpath)
    entry = {}
    entry["name"] = name
    entry["path"] = fullpath
    entry["owner"] = result.st_uid
    entry["group"] = result.st_gid
    entry["lastmod"] = result.st_mtime
    entry["perms"] = oct(stat.S_IMODE(result.st_mode))
    entry["wread"] = int(str(oct(stat.S_IMODE(result.st_mode)))[-1]) >= 4
    entry["size"] = result.st_size
    return entry;

def updateup(fullpath):
    while fullpath != "":
        mycol.update_one({"path": fullpath},{"$set": dirinfo(fullpath)})
        fullpath = fullpath[0:fullpath.rfind('/')]

def insertnd(toinsert, keytocheck):
    if(isinstance(toinsert, list)):
        for i in toinsert:
            insertnd(i, keytocheck)
    else:
        if(mycol.find_one({keytocheck: toinsert[keytocheck]}) is None):
            mycol.insert_one(toinsert)
        else:
            mycol.update_one({keytocheck: toinsert[keytocheck]}, {"$set": toinsert})

class Watcher:
    def __init__(self, toWatch):
        self.observer = Observer()
        self.search = toWatch

    def run(self):
        event_handler = Handler()
        for DIRECTORY_TO_WATCH in self.search:
            self.observer.schedule(event_handler, DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            if(event.event_type == 'created'):
                insertnd(dirinfo(event.src_path), "path")
                if("--verbose" in sys.argv):
                    print(event.src_path + " created")
            elif(event.event_type == 'modified'):
                if("--verbose" in sys.argv):
                    print(event.src_path + " modified")
                try:
                    updateup(event.src_path)
                except:
                    if("--verbose" in sys.argv):
                        print("but the directory already vanished!")
                mycol.update_one({"path": event.src_path},{"$set": dirinfo(event.src_path)})
            elif(event.event_type == 'moved'):
                mycol.update_one({"path": event.src_path},{"$set": {"path": event.dest_path}})
                if("--verbose" in sys.argv):
                    print(event.src_path + " moved to " + event.dest_path)
            elif(event.event_type == 'deleted'):
                mycol.delete_one({"path": event.src_path})
                if("--verbose" in sys.argv):
                    print(event.src_path + " deleted")

def killscript(pid):
    file = open(scriptpath + "/kill/" + str(pid) + ".sh", "w")
    file.write("#!/bin/bash\nkill " + str(pid) + "\nrm -f $0")
    os.chmod(scriptpath + "/kill/" + str(pid) + ".sh", stat.S_IRWXU)
    file.close()
#########################################################################################
scriptpath = os.path.realpath(__file__)
scriptpath = scriptpath[:scriptpath.rfind("/") + 1]
conf = open(scriptpath + "mongonas.conf", "r")

clines = conf.readlines()
conf.close()
conf=[x.strip() for x in clines]

ip = "127.0.0.1"
port = "27017"
usr = None
pw = None

if("db:" in conf[0:-2]):
    ip = conf[conf.index("db:")+1]

if("port:" in conf[0:-2]):
    port = conf[conf.index("port:")+1]

if("dbname:" in conf[0:-2]):
    dbname = conf[conf.index("dbname:")+1]
else:
    print("Must specify DB name in conf file");
    exit(1)

if("colname_dir:" in conf[0:-2]):
    colname = conf[conf.index("colname_dir:")+1]

else:
    print("Must specify collection name in conf file");
    exit(1)

if("usr:" in conf[0:-2]):
    usr = conf[conf.index("usr:")+1]

if("pw:" in conf[0:-2]):
    pw = conf[conf.index("pw:")+1]

exclude = []
if("exclude:" in conf[0:-2]):
    index = conf.index("exclude:")+1
    while(index < len(conf) and conf[index] is not ""):
        exclude.append(conf[index])
        index += 1

search = []
if("search:" in conf[0:-2]):
    index = conf.index("search:")+1
    while(index < len(conf) and conf[index] is not ""):
        search.append(conf[index])
        index += 1

uri = "mongodb://"

if(usr is not None and pw is not None):
    uri = uri + (usr + ":" + pw + "@")

uri = uri + (ip + ":" + port + "/")

myclient = pymongo.MongoClient(uri)
mydb = myclient[dbname]
mycol = mydb[colname]
for directory in search:
    for root, dirs, files in os.walk(directory):
        for name in dirs:
            fullpath = os.path.join(root, name)
            if(not any(x in fullpath for x in exclude)):
                entry = dirinfo(fullpath)
                insertnd(entry, "path")
if("--once" not in sys.argv):
    killscript(os.getpid())
    w = Watcher(search)
    w.run()
