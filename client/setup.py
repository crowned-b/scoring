import os
import sys
import py_compile

if len(sys.argv)==2:
   main=sys.argv[1]
else:
   print "Usage: python setup.py <Main User>\nExample: python setup.py cyber\n"
   sys.exit()

scorebotdir="/var/scorebot/"
py_compile.compile(scorebotdir+"client.py")
os.remove(scorebotdir+"client.py")

template="""
   while sleep 5; do python /var/scorebot/client.pyc /var/scorebot/client.json; done &
"""

with open("/etc/init.d/scorebot",'w') as f:
   f.write(template)
   f.close()

with open("/home/"+main+"/.bashrc","a") as f:
   f.write("/var/scorebot/setup.bash\n")
   f.close() 

os.system("chmod +x /var/scorebot/*")
os.system("chmod 777 /var/scorebot/name /var/scorebot/setup.bash")
os.system("chmod 755 /etc/init.d/scorebot")
os.system("update-rc.d scorebot enable")
os.remove("/var/scorebot/setup.py")

