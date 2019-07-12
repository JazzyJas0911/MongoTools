import pymongo
import sys

if(len(sys.argv) != 2):
    print("Usage: python3 mongo_print.py <key>")
    exit()

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

uri = "mongodb://"

if(usr is not None and pw is not None):
    uri = uri + (usr + ":" + pw + "@")
uri = uri + (ip + ":" + port + "/")

myclient = pymongo.MongoClient(uri)

mydb = myclient[dbname]
mycol = mydb[colname]

#for x in mycol.find({},{ "_id": 0, "owner": 0, "name": 0, "wread": 0,  "path": 1,  "lastmod": 0,  "group": 0,  "used-b": 0,  "used-p": 0,  "perms": 0,  "zone": 0,  "fstype": 0,  "capacity": 0,  "quota": 0, "fcount": 0 }):

for x in mycol.find({},{ "_id": 0, sys.argv[1]: 1,}):
      print(x[sys.argv[1]])
