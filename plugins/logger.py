from Plugin import *
from time import localtime, strftime

class logger(Plugin):
    def __init__(self):
        self.parent = Plugin.__init__(self)
        self.running = True
        self.nick = None


    def setup(self):
        print "We need to read a config file or something"

    def run(self):
        while self.running:
            line = super(logger, self).getData()
            print "Logger got this: ", line
            self.log_str(line)

    def stop(self):
        self.running = False

    def setNick(self, nick):
        self.nick = nick
            
    def log_str(self, line):
        items = line.split(" ");
        msg = line.split(":");
        channel = items[2][1:]
        source = items[0].split("!")[0][1:]
        data = msg[2]
        print "Channel: '%s' Source: '%s' Message: '%s'" % (channel, source, data)
        filename = channel + "_" + strftime("%d-%m-%Y", localtime()) + ".txt"
        print "Filename: '%s'" % filename
        log_line = strftime("%H:%M:%S", localtime()) + " <"+source+"> " + data + "\n"
        file = open(filename, 'a')
        file.write(log_line)
        file.close()
