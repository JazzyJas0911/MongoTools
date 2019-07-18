import os
import pymongo
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

if("colname_dir:" in conf[0:-2]):
    colname = conf[conf.index("colname_dir:")+1]

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


if(len(sys.argv) == 1):
    print("Must specify collection to drop, like:\n\n$ python mdrop.py <collection>\n\nCollections in this database:")
    for name in mydb.list_collection_names():
        print(name)
    exit()

for column in sys.argv[1:]:
    mycol = mydb[column]
    if (input("Hey, are you sure you want to drop the collection " + column + "?\nType the name of the collection again to confirm drop.\n") == column):
        mycol.drop()
        print("Drop order sent.")
    else:
        print("Names do not match, delete aborted.")
