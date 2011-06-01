from Plugin import *
from time import localtime, gmtime, strftime

class logger(Plugin):
    def __init__(self):
        self.parent = Plugin.__init__(self)
        self.running = True
        self.nick = None
        self.path = None
        self.use_utc = False

    def setup(self):
        print "We need to read a config file or something"
        self.path = "."

    def run(self):
        while self.running:
            line = super(logger, self).getData()
            info = line.split(" ")
            if info[1] == "PRIVMSG":
                self.log_user_msg(line)
            else:
                self.log_op_msg(line)

    def stop(self):
        self.running = False

    def setNick(self, nick):
        self.nick = nick

    def log_user_msg(self, line):
        items = line.split(" ")
        msg = line.split(":")
        channel = items[2][1:]
        source = items[0].split("!")[0][1:]
        data = msg[2]
        log_line = "<"+source+"> " + data + "\n"
        self.log_to_file(channel, log_line)

    def log_op_msg(self, line):
        items = line.split(" ")
        source = items[0].split("!")[0][1:]
        op = items[1]
        if items[2][0] == ':':
            channel = items[2][2:]
        else:
            channel = items[2][1:]
        log_line = source+" " + op + " #" + channel + "\n"
        self.log_to_file(channel, log_line)

    def log_to_file(self, channel, line):
        filename = channel + "_"
        if self.use_utc == True:
            filename = filename + strftime("%Y-%m-%d", gmtime())
            finalLine = strftime("%H:%M:%S", gmtime()) + " "
        else:
            filename = filename + strftime("%Y-%m-%d", localtime())
            finalLine = strftime("%H:%M:%S", gmtime()) + " "
        filename = filename + ".txt"
        finalFileName = os.path.join(self.path, filename)
        finalLine = finalLine + line
        file = open(finalFileName, 'a')
        file.write(finalLine)
        file.close()
