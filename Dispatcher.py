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
            print info[0] # a ver como parseas esto para sacar el nick del webas que te escribio
            nick = "P4C0"
            self.irc.sendPrivate(nick, "Shi Shi Shi Amo")

