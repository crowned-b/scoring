import socket
import sys
import json
import os

class Point():
   def __init__(self,description,value,boolean,names=[]):
      self.description=description
      self.value=value
      self.boolean=boolean+" >/dev/null"
      self.names=names
      self.isGroup=False
   def check(self):
      return os.system(self.boolean)

class PointGroup(): #see server.json for examples of points/pointgroups
   def __init__(self,description,value,boolean,names=[]):
      self.points=[]
      for i in names:
         self.points.append(Point(description%i,value,boolean%i))
      self.isGroup=True

def getScore(name,points):
   pointsGotten=[]
   totalScore=0
   currentScore=0
   numGotten=0
   totalPoints=0

   for i in points:
      if i.isGroup:
         for j in i.points:
            totalPoints+=1
            totalScore+=j.value
            if j.check()==0:
               currentScore+=j.value
               numGotten+=1
               pointsGotten.append(j)
      else:
         totalPoints+=1
         totalScore+=i.value
         if i.check()==0:
            currentScore+=i.value
            numGotten+=1
            pointsGotten.append(i)
   return [currentScore,totalScore,numGotten,totalPoints,name,pointsGotten]

def score(server,port,scorePackage=""):
   try:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   except socket.error:
      print 'Socket failed'
      sys.exit()

   s.connect((server,port))
   try:
      if scorePackage!="":
         s.sendall(scorePackage.encode())
      else:
         s.sendall("none")
   except socket.error:
      print 'Score upload failed'
      sys.exit()
   reply=s.recv(4096)
   if scorePackage=="":
      return reply

if len(sys.argv) == 2:
   configfile=sys.argv[1]
else:
   print "Usage: python client.py <configfile>"
   sys.exit()

try:
   with open(configfile) as f:
      config=json.load(f)
except:
   print "config file could not be loaded\n"
   sys.exit()
try:
   with open("/var/scorebot/name",'r') as f:
      name=f.read()
      f.close()
   name=name.replace("\n","")
except:
   print "Namefile does not exist"
   sys.exit()

if name="":
   sys.exit()

try:
   server=config.get("ip")
   port=config.get("port")
except:
   print "Invalid file config\n"
   sys.exit()
try:
   pointSkel=score(server,port)
   pointSkel=json.loads(pointSkel.decode())
   points=[]

   for i in pointSkel:
      parts = pointSkel.get(str(i))
      points.append(PointGroup(parts[0],parts[1],parts[2],parts[3]))


   pack=getScore(name,points)
   for i in pack[-1]:
      d=i.description
      v=i.value
      pack.append([d,v])
   pack.pop(5)
   pack=json.dumps({"1":pack})

   score(server,port,pack)
except:
   print "could not send points to scoring server\n"
   sys.exit()

