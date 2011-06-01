from Plugin import *
from Events import *
from Irc import *

class Dispatcher:
    
    def __init__(self, irc):
        self.irc = irc
        self.nick = irc.getNick()
        self.plugins = []
        self.plugin_classes = find_plugins("plugins", Plugin)
        print "We found %d plugins to load" % len(self.plugin_classes)
        print "Loading plugins..."
        for i in range(len(self.plugin_classes)):
            tmp = self.plugin_classes[i]()
            tmp.setNick(self.nick)
            tmp.setup()
            tmp.start()
            self.plugins.append(tmp)
        print "Done!"

    def recvIRCMsg(self, event):
        string = event.arg
        info = string.split(" ")
        if info[1] == "PRIVMSG" or info[1] == "JOIN" or info[1] == "PART" or info[1] == "KICK":
            for i in range(len(self.plugins)):
                self.plugins[i].sendToPlugin(string)

    def stop_plugins(self):
        for i in range(len(self.plugins)):
            self.plugins[i].stop()
            self.plugins[i].join()

