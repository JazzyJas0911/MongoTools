import json
from datetime import datetime
import pymongo
import subprocess
import os
import sys

def insertnd(toinsert, keytocheck):
    if(isinstance(toinsert, list)):
        for i in toinsert:
            insertnd(i, keytocheck)
    else:
        if(mycol.find_one({keytocheck: toinsert[keytocheck]}) is None):
            mycol.insert_one(toinsert)
        else:
            mycol.update_one({keytocheck: toinsert[keytocheck]}, {"$set": toinsert})

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

if("colname_sys:" in conf[0:-2]):
    colname = conf[conf.index("colname_sys:")+1]
else:
    print("Must specify collection name in conf file");
    exit(1)

filers = []
if("filers:" in conf[0:-2]):
    index = conf.index("filers:")+1
    while(index < len(conf) and conf[index] is not ""):
        filers.append(conf[index])
        index += 1

attributes = []
if("attributes:" in conf[0:-2]):
    index = conf.index("attributes:")+1
    while(index < len(conf) and conf[index] is not ""):
        attributes.append(conf[index])
        index += 1

if("usr:" in conf[0:-2]):
    usr = conf[conf.index("usr:")+1]

if("pw:" in conf[0:-2]):
    pw = conf[conf.index("pw:")+1]

uri = "mongodb://"

if(usr is not None and pw is not None):
    uri = uri + (usr + ":" + pw + "@")

uri = uri + (ip + ":" + port + "/")

myclient = pymongo.MongoClient(uri)
mydb = myclient[dbname]
mycol = mydb[colname]
entries = []
for cluster in filers:
    entry = {"name": cluster}
    for attr in attributes: 
        p = subprocess.Popen(['cdot', "-c", cluster, "get", "-j", attr], stdout=subprocess.PIPE)
        out, err = p.communicate()
        out = out.decode("utf-8")
        try:
            out=out[out.index('[{'):]
            #print(out)
            out=json.loads(out)
            entry[attr] = out
        except:
            eprint("\nTried the command:\n" + "\ncdot -c " + cluster + "get -j " + attr + "\n" + "\nThat query goofed somehow.\nOutput was sent to the end of goof.log:\n")
            goof = open("goof.log", "a")
            goof.write("\n\nAt " + str(datetime.now()) + "cdot messed up somehow.\nCommand was:\n" + "\ncdot -c " + cluster + "get -j " + attr + "\n\nOutput was:\n\n" + out)
            goof.close()
        entries.append(entry)
insertnd(entries, "name")
