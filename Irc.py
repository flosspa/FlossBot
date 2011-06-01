import socket, threading, random, time
from Events import *
from Dispatcher import *

class ListenThread(threading.Thread):

    def __init__(self, socket, irc):
        threading.Thread.__init__(self)

        self.socket = socket
        self.irc = irc
        self.readBuffer = ""
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            try:
                self.readBuffer += self.socket.recv(1024)
            except:
                pass

            while self.readBuffer.find('\n') >= 0:
                breakPoint = self.readBuffer.find('\n')
                line = self.readBuffer[0:breakPoint].replace('\r', '')
                self.readBuffer = self.readBuffer[breakPoint+1:]
                event = Event(IRC_RECV, line)
                getEventManager().signalEvent(event)
        

class Irc:

    def __init__(self, host, port, channel, nick):
        self.host = host
        self.port = port
        self.channel = channel
        self.socket = socket.socket()
        self.socket.settimeout(5)
        self.connected = False

        self.nick = nick
        self.ops = []

        listener = Listener(IRC_RECV, self.parseIRCString)
        getEventManager().addListener(listener)

        self.connect()

    def connect(self):
        self.listenThread = ListenThread(self.socket, self)

        try:
            self.socket.connect((self.host, self.port))
        except Exception as e:
            print "error connecting, aborting", e.args
            return

        self.connected = True

        self.listenThread.start()

        self.socket.send("NICK %s\r\n" % self.nick)
        self.socket.send("USER flossbot %s Bototo :Floss-PA Bot\r\n" % self.host)

        self.dispatcher = Dispatcher(self)

        listener = Listener(IRC_MSG, self.dispatcher.recvIRCMsg)
        getEventManager().addListener(listener)

    def disconnect(self):
        self.connected = False
        self.stop()
        self.socket = socket.socket()
        self.socket.settimeout(5)
        if self.listenThread and self.listenThread.is_alive():
            self.listenThread.join()
        self.listenThread = None
        self.dispatcher.stop_plugins()
        self.dispatcher = None

    def deleteOp(self, op):
        self.ops[:] = (value for value in self.ops if value != op)

    def parseIRCString(self, event):
        string = event.arg
        if string.find("PING") == 0:
            self.socket.send("PONG " + string[5:] + "\r\n")
            print "PONG", string[5:]
        elif string[0] == ":":
            print string
            info = string.split(" ")
            if info[1] == "MODE": #and info[2] == self.channel:
                if info[3] == "+o":
                    self.ops.append(info[4])
                elif info[3] == "-o":
                    self.deleteOp(info[4])
            elif info[2] == self.nick and (info[3] == "=" or info[3] == "@"): #and info[4] == self.channel:
                for op in info[5:]:
                    if len(op) == 0:
                        continue
                    op = op.replace(':', '')
                    if op[0] == "@":
                        self.ops.append(op[1:])
                print "Connection succesful"
            elif info[1] == "002":
                for to_join in self.channel:
                    self.socket.send("JOIN %s\r\n" % to_join)
            elif info[1] == "KICK":
                self.socket.send("JOIN %s\r\n" % info[2])
            else: 
                event = Event(IRC_MSG, string)
                getEventManager().signalEvent(event)
        else:
            print "SCRAP", string
            if string == "ERROR :All connections in use":
                print "retrying in 5 seconds"
                self.disconnect()

                event = Event(IRC_RESTART, None)
                getEventManager().signalEvent(event)

    def sendTo(self, dest, message):
        self.socket.send("PRIVMSG %s :%s\r\n" % (dest, message))

    def stop(self):
        if self.listenThread:
            self.listenThread.stop()
            
    def getNick(self):
        return self.nick
