import os
import stat
import sys
import subprocess
import pymongo

conf = open("mongonas.conf", "r")
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

if("colname:" in conf[0:-2]):
    colname = conf[conf.index("colname:")+1]

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

example = {"owner": 0, "name": 0, "wread": 0,  "path": 0,  "lastmod": 0,  "group": 0,  "used-b": 0,  "used-p": 0,  "perms": 0,  "zone": 0,  "fstype": 0,  "size": 0,  "quota": 0, "fcount": 0}
for directory in search:
    for root, dirs, files in os.walk(directory):
        for name in dirs:
            fullpath = os.path.join(root, name)
            if(not any(x in fullpath for x in exclude)):
                print("scanning " + fullpath)
                result=os.stat(fullpath)
                entry = dict(example) #make a copy of the example doc
                entry["name"] = name
                entry["path"] = fullpath
                entry["owner"] = result.st_uid
                entry["group"] = result.st_gid
                entry["lastmod"] = result.st_mtime
                entry["perms"] = oct(stat.S_IMODE(result.st_mode))
                entry["wread"] = int(str(oct(stat.S_IMODE(result.st_mode)))[-1]) >= 4
                entry["size"] = result.st_size
                x = mycol.insert_one(entry)
