import pymongo
import os
import sys

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
if(len(sys.argv) == 1):
    print("Please specify collection to print, like:\n\n$ python mprint.py <collection>\n\nCollections in this database:")
    for name in mydb.list_collection_names():
        print(name)
    exit()
else:
    colname = sys.argv[1]

mycol = mydb[colname]


for x in mycol.find():
    if(len(sys.argv) >= 3):
       keychain = sys.argv[2:] 
       for key in keychain:
          if(key.isdigit()):
              key = int(key)
          x = x[key]
    if(isinstance(x, dict)):
        print("Keys available: " + str(x.keys()))
    if(isinstance(x, list)):
        print("Indices available: 0:" + str(len(x) - 1))
    print(x)
