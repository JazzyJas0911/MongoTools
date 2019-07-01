import os
import stat
import sys
import subprocess
import pymongo

if(len(sys.argv) != 2):
    print("Usage: python3 dirscan.py <directory>")
    exit()

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["directories"]

example = {"owner": 0, "name": 0, "wread": 0,  "path": 0,  "lastmod": 0,  "group": 0,  "used-b": 0,  "used-p": 0,  "perms": 0,  "zone": 0,  "fstype": 0,  "size": 0,  "quota": 0, "fcount": 0}
exclude = ["mnt", "proc"]
for root, dirs, files in os.walk(str(sys.argv[1])):
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
            entry["size"] = result.st_size
            x = mycol.insert_one(entry)
