from Events import *
from Irc import *

class Dispatcher:
    
    def __init__(self, irc):
        self.irc = irc
        self.channel = irc.getChannel()
        self.nick = irc.getNick()

    def recvIRCMsg(self, event):
        string = event.arg
        info = string.split(" ")
        if info[1] == "PRIVMSG": 
            #msg to reply
            if string.lower().find(self.nick.lower()) > -1:
                destination = info[2]
                source = info[0].split("!")[0][1:]
                if (source != self.nick and destination != self.nick):
                    self.irc.sendTo(destination, "Bot in Beta Testing... ")
                elif (destination == self.nick and source != self.nick):
                    self.irc.sendTo(source, "Bot in Beta Testing... ")


