import os
import sys
import py_compile

if len(sys.argv)==2:
   main=sys.argv[1]
else:
   print "Usage: python setup.py <Main User>\nExample: python setup.py cyber\n"
   sys.exit()

pwd=os.getcwd()

scorebotdir="/var/scorebot/"
os.makedir(scorebotdir)
files=os.listdir(pwd)
for i in files:
   os.rename(pwd+i,scorebotdir+i)

py_compile.compile(scorebotdir+"client.py")
os.remove(scorebotdir+"client.py")

template="while sleep 5; do python %sclient.pyc %sclient.json; done &" % (scorebotdir,scorebotdir)

with open("/etc/init.d/scorebot",'w') as f:
   f.write(template)
   f.close()

with open("/home/"+main+"/.bashrc","a") as f:
   f.write("%ssetup.bash\n" % scorebotdir)
   f.close()

os.system("chmod +x %s*" % scorebotdir)
os.system("chmod 777 %sname %ssetup.bash" % (scorebotdir, scorebotdir))
os.system("chmod 755 /etc/init.d/scorebot")
os.system("update-rc.d scorebot enable")
os.remove("%ssetup.py" % scorebotdir)
