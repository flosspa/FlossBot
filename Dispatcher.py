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
        if info[1] == "PRIVMSG" and info[2] == self.channel:
            #msg to the channel
            if string.lower().find(self.nick.lower()) > -1:
                self.irc.sendChannel("P4C0 rulez! todos deberian chuparsela... he dicho!")
        elif info[1] == "PRIVMSG" and info[2] == self.nick:
            #private msg
            nick = info[0].split("!")[0][1:] #so 1337
            self.irc.sendPrivate(nick, "SHOW ME TITS OR STFU")

