import sys
import subprocess
import pwd, grp
from faker import Faker

usercount = 1
fake = Faker()
if(len(sys.argv) == 2 and sys.argv[1].isdigit()):
   usercount = int(sys.argv[1])

existingusers = [p[0] for p in pwd.getpwall()]

#[print(x) for x in existingusers]

for i in range(usercount):
   uname = fake.last_name().lower()
   n = 1
   while((uname + str(n)) in existingusers):
      n += 1
   uname = uname + str(n)
   print(uname)
   subprocess.run(["useradd", uname,])
   if(usercount != 0):
      subprocess.run(["dd", "if=/dev/null", "of=/home/" + uname + "/" + uname + "_garbage.txt", "bs=1M", "count=" + str(int((200 / usercount) * i))])
   else:
      subprocess.run(["touch", "/home/" + uname + "/" + uname + "_garbage.txt"])
   subprocess.run(["chown", uname + ":" + uname, "/home/" + uname + "/" + uname + "_garbage.txt"])
   existingusers.append(uname)
