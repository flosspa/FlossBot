from Plugin import *
import urllib
import string

class lmgtfy(Plugin):
    def __init__(self):
        self.parent = Plugin.__init__(self)
        self.running = True
        self.nick = None
        
    def setup(self):
        print "Starting lmgtfy.com plugin"
        self.running = True
        
    def run(self):
        while self.running:
            line = super(lmgtfy, self).getData()
            if line == None:
                continue
            info = line.split(" ")
            if info[1] == "PRIVMSG" and info[3][1:] == "!dile":
                channel = info[2]
                if len(info) < 6:
                    self.usage(channel)
                else:
                    self.process(channel, info[4], string.join(info[5:]))
            

    def stop(self):
        self.running = False

    def setNick(self, nick):
        self.nick = nick

    def process(self, channel, nick, query):
        urlenc_string = urllib.urlencode(dict(q=query))
        link = "http://lmgtfy.com/?%s" % urlenc_string
        msg = "%s: Visita: %s" % (nick, link)
        super(lmgtfy, self).sendToIrc(channel, msg)

    def usage(self, channel):
        msg = "Use: !dile <nick> <cadena a buscar>"
        super(lmgtfy, self).sendToIrc(channel, msg)
        

