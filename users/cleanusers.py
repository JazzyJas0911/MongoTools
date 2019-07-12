import pwd
import subprocess

nodelete = open("nodelete.txt", "r")
lines = nodelete.readlines()
nodelete.close()
nodelete = [x.strip() for x in lines]

existingusers = [p[0] for p in pwd.getpwall()]

delete = [x for x in existingusers if x not in nodelete]
for user in delete:
   subprocess.run(["rm", "-rf", "/home/" + user])
   subprocess.run(["userdel", user])
