#!/usr/bin/env python

import sys, socket, string, random, os, time, ConfigParser
from Events import *
from Irc import *

irc = None
running = True

def restartIRCHook(event):
    global irc

    time.sleep(5)
    irc.connect()

def main(args):
    global irc
    
    config = ConfigParser.ConfigParser()
    if (sys.argv != 2):
        cfile = "bot.conf"
    else:
        cfile = args[1]

    listener = Listener(IRC_RESTART, restartIRCHook)
    getEventManager().addListener(listener)

    try:
        config.readfp(open(cfile))
    except:
        print "Error loading configuration file:", sys.exc_info()[1]
        sys.exit(1)

    host = config.get("main", "host")
    port = config.get("main", "port")
    channels = config.get("main", "channels")
    nick = config.get("main", "nick")

    print "Host: ", host
    print "Port: ", port
    print "Channels: ", channels

    channels = channels.split(",")
    
    port = int(port)
    
    for i in range(len(channels)):
        if channels[i][0] != '#':
            channels[i] = '#' + channels[i]

    getEventManager().start()

    irc = Irc(host, port, channels, nick)

    while running:
        try:
            i = raw_input()
            if i == "quit" or i == "exit":
                irc.disconnect()
                getEventManager().stop()
                break
        except KeyboardInterrupt:
            irc.disconnect()
            getEventManager().stop()
            break

    time.sleep(1)
    sys.exit()

if __name__ == '__main__':
    main(sys.argv)

