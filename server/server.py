import os
import socket
import sys
import thread
import threading
import json
from operator import itemgetter

debug=False
leaderboards=[]

def onNewClient(connection,client_address):
   global debug
   try:
      with open('server.json') as f:
         points=json.dumps(json.load(f)) #load points

      if debug: print >>sys.stderr, 'connection from', client_address
      while True:
         data=connection.recv(4096)
         if data:
            connection.sendall(points.encode()) #send points
            if debug: print >>sys.stderr, 'received "%s"' % data
            pack=[]
            if data!="none":
               data=json.loads(data.decode()) #retrieve information from client
               pack=data.get("1")
               name=str(pack[4]) #retrieve name
               cScore=pack[0] #retrieve current score
               inBoard=False
               aIndex=False
               if os.path.exists("/var/www/html/leaderboard.html"): #if the leaderboard gets moved/deleted make a new one
                  leaderboard=[]
               for i in leaderboard:
                  if i[0]==name:
                     inBoard=True
                     aIndex=leaderboard.index(i)
               if not inBoard:
                 leaderboard.append([name,cScore])
                 index=leaderboard.index([name,cScore])
                 makeLeader(leaderboard) #generate leaderboard
                 makeHtml(pack)
               elif leaderboard[aIndex][1]!=cScore:
                  leaderboard[aIndex][1]=cScore
                  makeLeader(leaderboard) #generate leaderboard
                  makeHtml(pack)

         else:
            if debug: print >>sys.stderr, 'no more data from', client_address
            break
   finally:
      connection.close()



def getConnection(sock):
   global debug
   while True:
      if debug: print >>sys.stderr,'waiting for a connection'
      connection, client_address = sock.accept()
      thread.start_new_thread(onNewClient,(connection,client_address)) #enable multiple connections

class Handler(threading.Thread):
   def __init_(self,sock):
      super(Handler, self).__init__(target=getConnection,args=(sock,))

class CustomSock(socket.socket):
   def __init__(self,port):
      super(CustomSock,self).__init__(socket.AF_INET, socket.SOCK_STREAM)
      self.server_address=('0.0.0.0',port)
      self.bind(self.server_address)
      self.listen(1)
   def changePort(self,port):
      self.close()
      self.__init__(port)

if len(sys.argv) == 2:
   sock=CustomSock(int(sys.argv[1]))
else:
   print "Usage: server.py <port>"
   sys.exit()

mainThread=Handler(target=getConnection,args=(sock,))
mainThread.daemon=True
mainThread.start()

def getInput():
   global sock
   global debug
   global mainThread
   port=sys.argv[1]
   while True:
      resp=raw_input("Enter Command: ")
      if resp=="quit":
         print 'quitting\n'
         sys.exit()
      elif resp=="reset":
         os.system("mv /var/www/html/leaderboard.html /var/www/html/l.bak")
         print "leaderboard.html moved to l.bak"
      elif resp[:4]=="port":
         try:
            if int(resp[5:]) in range(1,65536):
               port=int(resp[5:])
               sock.changePort(int(resp[5:]))
            else:
               print 'invalid port\n'
         except:
            print 'socket error\n'
      elif resp=="status":
         print "Server scoring on port %s\n" % port
      elif resp=="debug":
         if not debug:
            debug=True
         else:
            debug=False
         print ("debugging = %s\n" % debug)
      elif resp=="help":
         print "Commands:\nquit - terminate server\nreset - reset leaderboard\nport <num> - change port of server\nstatus - print server status\ndebug - run to enable/disable debugging\nhelp - display this help\n"
      else:
         print "Run 'help' to list commands\n"


def makeHtml(pack):
   currentScore=pack[0]
   totalScore=pack[1]
   numGotten=pack[2]
   totalPoints=pack[3]
   name=pack[4]
   pointsGotten=pack[6:]

   template = """
      <!DOCTYPE html>
      <html>
      <p><b><font size='7'>Score: {score}</p></b></font>
      <p><font size='5'>{vulns}/{totalVulns} vulnerabilities</font></p>
      <ul>
   """
   context={
      'score':currentScore,
      'vulns':numGotten,
      'totalVulns':totalPoints
   }

   filename="/var/www/html/%s.html" % name
   with open(filename,'w') as myfile:
      myfile.write(template.format(**context))

   for i in pack[5:]:
      with open(filename,'a') as myfile:
         myfile.write("<li>%s: %s</li>" % (i[0],i[1]))

def makeLeader(leaderboard):
   template="""
      <!DOCTYPE html>
      <html>
      <p><b><font size='7'>Leaderboard</p></b></font>
      <ol>
   """
   filename="/var/www/html/leaderboard.html"
   with open(filename,'w') as myfile:
      myfile.write(template)

   leaderboard=sorted(leaderboard, key=itemgetter(1), reverse=True)
   for i in leaderboard:
      with open(filename,'a') as myfile:
         myfile.write("<li>%s: %s</li>" % (i[0], i[1]))

getInput()
