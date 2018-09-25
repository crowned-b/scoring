import os
import sys
import py_compile


scorebotdir=raw_input("Enter directory for scorebot files\nExample: /var/scorebot/\nEnter Directory: ")
print ''
while (scorebotdir[0]!='/' or scorebotdir[-1]!='/'):
   print "Incorrect directory format. Example: /var/scorebot/\n"
   scorebotdir=raw_input("Enter directory for scorebot files\nExample: /var/scorebot/\nEnter Directory: ")

main=raw_input("Enter main user for image\nExample: cyber\nEnter User: ")
print ''
while (os.system("getent passwd %s" % main)!=0):
   print "User %s does not exist\n" % main
   main=raw_input("Enter main user for image\nExample: cyber\nEnter User: ")
   print ''

scorebotInit=raw_input("Enter name for scorebot init script\nExample: scorebot\nEnter Filename: ")
print ''
while (os.path.isfile("/etc/init.d/%s" % scorebotInit)):
   print "Init script with name %s already exists" % scorebotInit
   scorebotInit=raw_input("Enter name for scorebot init script\nExample: scorebot\nEnter Filename: ")
   print ''


pwd=os.getcwd()

os.makedirs(scorebotdir)
files=os.listdir(pwd)

for i in files:
   os.rename(pwd+i,scorebotdir+i)

py_compile.compile(scorebotdir+"client.py")
os.remove(scorebotdir+"client.py")

template="while sleep 5; do python %sclient.pyc %sclient.json; done &" % (scorebotdir,scorebotdir)

with open("/etc/init.d/%s" % scorebotInit,'w') as f:
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
